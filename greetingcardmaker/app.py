import csv
import os
import ollama
from fpdf import FPDF

# Function to generate wishes using Ollama, You can change the prompt based on the event, we can reuse this for rec also lol
# Feel free to better prompting, this works like 80-90% without hallucinating or doing something weird, so make sure to proof read"
def generate_wishes(name):
    prompt = (f"Write a heartfelt thank you message for Teacher's Day to {name}, a volunteer leader for the volunteers at U&I. "
              "Mention their dedication, impact on children's lives, and role as an excellent leader and role model. Their work is often unoticed but we want to recognise and appreciate their efforts. "
              "Keep it under 200 words and print only the message, don't say anything else. End the message with 'Warm regards, Leader A and Leader B'.") # make sure you change this Leader A and B accordingly
    response = ollama.generate(model="llama3", prompt=prompt)
    return response['response']


# Function to create the PDF along with the image
def create_pdf(name, wishes, output_folder):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", 'B', 16)
            self.cell(0, 10, f"Happy Teacher's Day, {name}!", 0, 1, 'C')
            self.ln(10)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=wishes)
    
    pdf.ln(10)

    # Set the path to your image file, can be anything 
    image_path = "image_path_here" 
    if os.path.exists(image_path):
        pdf.image(image_path, x=60, y=pdf.get_y(), w=90, h=60)  

    # Output PDF to file, we can change this accordingly 
    filename = os.path.join(output_folder, f"{name}_teachers_day_wishes.pdf")
    pdf.output(filename)


# Main function
def main():
    output_folder = "teachers_day_wishes"
    os.makedirs(output_folder, exist_ok=True)
    
    with open('volunteers.csv', 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  
        for row in csv_reader:
            name = row[0]  # Assuming the name is in the first column
            print(f"Generating wishes for {name}...")
            wishes = generate_wishes(name)
            create_pdf(name, wishes, output_folder)
            print(f"PDF created for {name}")

if __name__ == "__main__":
    main()
