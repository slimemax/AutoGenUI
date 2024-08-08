import anthropic
import os
import time
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import queue

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY", "COPY-PASTE-YOUR-ANTHROPIC-KEY-HERE")
)

class App:
    def __init__(self, master):
        self.master = master
        master.title("Claude Auto Script Generator")
        master.geometry("1000x800")
        master.configure(bg='black')

        self.iteration = 0
        self.code = ""
        self.running = False
        self.queue = queue.Queue()

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.frame.configure(style='Black.TFrame')

        style = ttk.Style()
        style.configure('Black.TFrame', background='black')
        style.configure('Red.TLabel', foreground='red', background='black')
        style.configure('Red.TButton', foreground='red', background='black')

        # First Prompt
        ttk.Label(self.frame, text="First Prompt:", style='Red.TLabel').grid(row=0, column=0, sticky=tk.W, pady=5)
        self.first_prompt = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=80, height=5, bg='black', fg='red')
        self.first_prompt.grid(row=1, column=0, columnspan=2, pady=5)
        self.first_prompt.insert(tk.END, """Create a well-commented HTML GUI I can use with my API key, have lots of functions. Give only the RAW code and nothing else.""")

        # Follow-up Prompt
        ttk.Label(self.frame, text="Follow-up Prompt:", style='Red.TLabel').grid(row=2, column=0, sticky=tk.W, pady=5)
        self.followup_prompt = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=80, height=5, bg='black', fg='red')
        self.followup_prompt.grid(row=3, column=0, columnspan=2, pady=5)
        self.followup_prompt.insert(tk.END, """Improve the following code. Fix any bugs or errors you detect, optimize the code, and add new functionality or features. Take advantage of the extended output capacity to implement more advanced features or optimizations. Here's the current code:

{{code}}

Please provide the full improved code. Give only the code and nothing else.""")

        # Max Iterations
        ttk.Label(self.frame, text="Max Iterations:", style='Red.TLabel').grid(row=4, column=0, sticky=tk.W, pady=5)
        self.max_iterations = ttk.Entry(self.frame, width=10, style='Red.TButton')
        self.max_iterations.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.max_iterations.insert(0, "5")  # Default value

        self.start_button = ttk.Button(self.frame, text="Start", command=self.start, style='Red.TButton')
        self.start_button.grid(row=5, column=0, pady=5)

        self.stop_button = ttk.Button(self.frame, text="Stop", command=self.stop, state=tk.DISABLED, style='Red.TButton')
        self.stop_button.grid(row=5, column=1, pady=5)

        self.iteration_label = ttk.Label(self.frame, text="Iteration: 0", style='Red.TLabel')
        self.iteration_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.timer_label = ttk.Label(self.frame, text="Time: 0s", style='Red.TLabel')
        self.timer_label.grid(row=7, column=0, columnspan=2, pady=5)

        self.preview = scrolledtext.ScrolledText(self.frame, wrap=tk.WORD, width=80, height=30, bg='black', fg='red')
        self.preview.grid(row=8, column=0, columnspan=2, pady=5)
    def start(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.iteration = 0
        self.log("Starting the process...")
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("Process stopped.")

    def run(self):
        start_time = time.time()
        max_iterations = int(self.max_iterations.get())
        self.log(f"Max iterations set to: {max_iterations}")
        while self.running and self.iteration < max_iterations:
            self.iteration += 1
            self.queue.put(("iteration", self.iteration))
            self.log(f"Starting iteration {self.iteration}")
            
            prompt = self.get_prompt()
            self.log(f"Generated prompt for iteration {self.iteration}")
            
            self.log("Calling Claude API...")
            code = self.call_claude_api(prompt)
            
            if code:
                self.log("Received response from Claude API")
                self.save_code_to_file(code)
                self.code = code  # Update the current code
                preview = code[:1000] + "..." if len(code) > 1000 else code
                self.queue.put(("preview", f"Generated code:\n\n{preview}"))
            else:
                self.log("No code received from Claude API")
            
            elapsed_time = int(time.time() - start_time)
            self.queue.put(("timer", elapsed_time))
            
            self.master.after(100, self.process_queue)
            self.log("Waiting 30 seconds before next iteration...")
            time.sleep(30)

        if self.iteration >= max_iterations:
            self.log("Reached maximum iterations. Stopping.")
            self.stop()

    def process_queue(self):
        while not self.queue.empty():
            msg = self.queue.get()
            if msg[0] == "iteration":
                self.iteration_label.config(text=f"Iteration: {msg[1]}")
            elif msg[0] == "timer":
                self.timer_label.config(text=f"Time: {msg[1]}s")
            elif msg[0] == "preview":
                self.preview.delete(1.0, tk.END)
                self.preview.insert(tk.END, msg[1])


    def get_prompt(self):
        if self.iteration == 1:
            prompt = self.first_prompt.get("1.0", tk.END).strip()
        else:
            followup_template = self.followup_prompt.get("1.0", tk.END).strip()
            prompt = followup_template.replace("{{code}}", self.code)
        self.log(f"Prompt for iteration {self.iteration}:\n{prompt[:100]}...")
        return prompt

    def call_claude_api(self, prompt):
        try:
            self.log("Sending request to Claude API...")
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4096,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                extra_headers={
                    "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
                }
            )
            self.log("Received response from Claude API")
            content = response.content[0].text if response.content else ""
            
            # Extract only the code part from the response
            code_start = content.find("```html")
            code_end = content.rfind("```")
            if code_start != -1 and code_end != -1:
                code = content[code_start+7:code_end].strip()
            else:
                code = content  # If no code blocks found, use the entire content
            
            self.log(f"Extracted code. Length: {len(code)} characters")
            return code
        except Exception as e:
            self.log(f"Error calling Claude API: {e}")
            return None

    def save_code_to_file(self, code):
        if not code:
            self.log("No code to save.")
            return
        
        self.log(f"Attempting to save code. Length: {len(code)} characters")
        filename = f"{self.iteration}.html"
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(code)
            self.log(f"Saved code to {filename}")
        except Exception as e:
            self.log(f"Error saving file: {e}")

    def log(self, message):
        self.queue.put(("preview", f"{self.preview.get('1.0', tk.END)}\n[LOG] {message}"))
        print(f"[LOG] {message}")

def main():
    root = tk.Tk()
    root.configure(bg='black')
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
