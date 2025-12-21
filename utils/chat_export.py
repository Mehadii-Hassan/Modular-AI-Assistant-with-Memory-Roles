from fpdf import FPDF

def export_txt(messages):
    text = ""
    for msg in messages:
        text += f"{msg['role'].upper()}:\n{msg['content']}\n\n"
    return text

def export_pdf(messages, filename="MEHU_Chat.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)

    for msg in messages:
        pdf.multi_cell(0, 8, f"{msg['role'].upper()}:\n{msg['content']}\n")

    pdf.output(filename)
    return filename
