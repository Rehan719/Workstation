import os
import logging

class BaseGenerator:
    def __init__(self, output_dir: str = "output/incubation"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, content: str, filename: str):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(content)
        return path

class ReportGenerator(BaseGenerator):
    def generate_report(self, title: str, data: dict):
        content = f"# Scientific Report: {title}\n\n## Abstract\n{data.get('abstract', 'N/A')}\n\n## Results\n{data.get('results', 'N/A')}"
        return self.generate(content, f"{title.lower().replace(' ', '_')}.md")

class PresentationGenerator(BaseGenerator):
    def generate_slides(self, title: str, slides: list):
        content = f"# Presentation: {title}\n"
        for i, slide in enumerate(slides):
            content += f"\n## Slide {i+1}: {slide['title']}\n{slide['content']}\n"
        return self.generate(content, f"{title.lower().replace(' ', '_')}_slides.md")
