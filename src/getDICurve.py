import os
from datetime import datetime
from urllib.request import urlopen

URL = "https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp"

output_directory = os.path.dirname(__file__)
timestamp = datetime.now().strftime("%Y%m%d")
output_filename = f"curvaDI_{timestamp}.csv"
output_path = os.path.join(output_directory, output_filename)

with urlopen(URL) as response, open(output_path, "wb") as file_handle:
    file_handle.write(response.read())

file_size_bytes = os.path.getsize(output_path)
print(f"Downloaded to: {output_path} ({file_size_bytes} bytes)")

