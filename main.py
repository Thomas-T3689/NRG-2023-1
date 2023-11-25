import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

torch_device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2").to(torch_device)
model.config.pad_token_id = model.config.eos_token_id
conversation = []

def generate_response(prompt, max_tokens=300, top_k=50):
    model_inputs = tokenizer(prompt, return_tensors='pt').to(torch_device)

    # Ensure that the input tensor is not empty
    if model_inputs["input_ids"].size(1) == 0:
        return ["I'm sorry, I don't have enough information to generate a response."]

    beam_outputs = model.generate(
        **model_inputs,
        max_length=max_tokens,
        num_beams=5,
        no_repeat_ngram_size=2,
        num_return_sequences=5,
        early_stopping=True,
        top_k=top_k
    )

    responses = [tokenizer.decode(output, skip_special_tokens=True) for output in beam_outputs]
    return responses


# Function to interact with the chatbot
def chat_with_bot(notes):
    # print("You can type 'exit' or 'quit' to end the conversation.")

    # Initialize the conversation with an empty list

    while True:
        # Get user input
        user_input = "Summarize this please: "+notes

        # Check if the user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            break

        # If it's the first user input, add a system message to set the context
        if not conversation:
            conversation.append({"role": "system", "content": "You are a helpful assistant."})

        # Add user input to the conversation
        conversation.append({"role": "user", "content": user_input})

        # Tokenize only the user's input
        prompt = conversation[-1]["content"]

        # Generate a response using the updated function
        responses = generate_response(prompt)

        # Add the chatbot's response to the conversation
        conversation.append({"role": "assistant", "content": responses[0]})

        # Print the chatbot's response
        return(f"Chatbot: {responses[0]}")


def aiwindow():
  #Create new window for the ai thing
  AiWindow = tk.Toplevel(window)
  AiWindow.title("AI Generated Summary")
  AiWindow.geometry("300x300")
  #Get Summary
  notes = text_entry.get("1.0", tk.END)
  conversation.append(notes)
  airesponse = chat_with_bot(notes)
  #Add Label (Change this when the AI thing works)
  AiLabel = tk.Label(AiWindow, text=airesponse, wraplength=280)
  AiLabel.grid(column=0,row=0, padx=10, pady=10)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_entry.delete("1.0", tk.END)  # Clear existing text
            text_entry.insert(tk.END, content)
    aiwindow()

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        content = text_entry.get("1.0", tk.END)
        with open(file_path, "w") as file:
            file.write(content)
def toggle_bold():
  try:
    text = text_entry.tag_names(tk.SEL_FIRST)
    if "bold" in text:
      text_entry.tag_remove("bold", tk.SEL_FIRST, tk.SEL_LAST)
    else:
      text_entry.tag_add("bold", tk.SEL_FIRST, tk.SEL_LAST)
      text_entry.tag_configure("bold", font=("Helvetica", 9, "bold"))
  except:
    pass

def toggle_italic():
  try:
    text = text_entry.tag_names(tk.SEL_FIRST)
    if "italic" in text:
      text_entry.tag_remove("italic", tk.SEL_FIRST, tk.SEL_LAST)
    else:
      text_entry.tag_add("italic", tk.SEL_FIRST, tk.SEL_LAST)
      text_entry.tag_configure("italic", font=("Helvetica", 9, "italic"))
  except:
    pass
def toggle_underline():
  try:
    text = text_entry.tag_names(tk.SEL_FIRST)
    if "underline" in text:
      text_entry.tag_remove("underline", tk.SEL_FIRST, tk.SEL_LAST)
    else:
      text_entry.tag_add("underline", tk.SEL_FIRST, tk.SEL_LAST)
      text_entry.tag_configure("underline", underline=True)
  except:
    pass
def resize_image(event):
  def delayed_resize():
      new_width = event.width
      new_height = event.height
      resized_image = og_image.resize((new_width, new_height))
      updated_photo = ImageTk.PhotoImage(resized_image)
      background_label.configure(image=updated_photo)
      background_label.image = updated_photo
  window.after(10, delayed_resize)



# Create the main window
window = tk.Tk()
window.title("Two Note")
window.geometry("400x300")

# Load the PNG image
og_image = Image.open("Mondstat.png")
resized_image = og_image.resize((400,300))
photo = ImageTk.PhotoImage(resized_image)

# set background
background_label = tk.Label(window, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create Scrollbar
scrollbar = tk.Scrollbar(window, orient="vertical")
scrollbar.grid(column = 2, row=0, padx=(0,40), sticky="ns", pady=10)

# Create an Entry widget for text input
text_entry = tk.Text(window, wrap="word", height=10, width=40, yscrollcommand=scrollbar.set)
text_entry.grid(column=0, row=0, columnspan=2, pady=(10, 0), padx=(50, 0), sticky="nsew")
scrollbar.config(command=text_entry.yview)

# text formatting tool bar
formatting_toolbar = tk.Frame(window)
formatting_toolbar.grid(column=0, row=1, sticky="nw", padx=(50,0), pady=(0,10))

bold_button = tk.Button(formatting_toolbar, text="B", command=toggle_bold)
bold_button.grid(column=0, row=0, padx=(0,0), pady=(0,0))

italic_button = tk.Button(formatting_toolbar, text="I", command=toggle_italic)
italic_button.grid(column=1, row=0, padx=(0,0), pady=(0,0))

underline_button = tk.Button(formatting_toolbar, text="U", command=toggle_underline)
underline_button.grid(column=2, row=0, padx=(0,0), pady=(0,0))

# Create buttons for opening and saving files
open_button = tk.Button(window, text="Open File", command=open_file)
open_button.grid(column=0, row=2, sticky="nw", padx=(75, 0), pady=(0,25))

save_button = tk.Button(window, text="Save File", command=save_file)
save_button.grid(column=1, row=2, sticky="ne", padx=(0, 25))

#Making things resizable
window.columnconfigure(0, weight=0)
window.columnconfigure(1, weight=4)
window.columnconfigure(2, weight=0)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)

# Bind the resize_image function to the window resizing event
window.bind("<Configure>", resize_image)

#listbox



# Run the Tkinter event loop
window.mainloop()
