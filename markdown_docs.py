import os
import html2text

def convert_html_to_markdown(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    h = html2text.HTML2Text()
    h.ignore_links = False

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".html"):
                html_file_path = os.path.join(root, file)
                with open(html_file_path, 'r', encoding='utf-8') as html_file:
                    html_content = html_file.read()

                markdown_content = h.handle(html_content)
                
                # Construct output file path
                relative_path = os.path.relpath(html_file_path, input_dir)
                markdown_file_path = os.path.join(output_dir, os.path.splitext(relative_path)[0] + '.md')

                # Create directories if needed
                os.makedirs(os.path.dirname(markdown_file_path), exist_ok=True)

                with open(markdown_file_path, 'w', encoding='utf-8') as md_file:
                    md_file.write(markdown_content)
                    print(f"Converted {html_file_path} to {markdown_file_path}")

if __name__ == "__main__":
    input_directory = '.tmpdocs/solidity_python_sdk'
    output_directory = 'docs/solidity_python_sdk'
    convert_html_to_markdown(input_directory, output_directory)
