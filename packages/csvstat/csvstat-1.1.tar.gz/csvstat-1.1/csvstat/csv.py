class ExcelStatsAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.strings = []
        self.floats = []
        self.integers = []

    def analyze_excel(self):
        try:
           
            with open(self.filename, 'rb') as file:
               
                excel_content = file.read()

                
                sheet_header = b'xl/worksheets/sheet'
                sheet_start = excel_content.find(sheet_header)
                sheet_end = excel_content.find(b'.xml', sheet_start)

                
                sheet_content = excel_content[sheet_start:sheet_end]

                
                column_data = [value.decode('utf-8') for value in sheet_content.split(b'<v>') if b'</v>' in value]

               
                for value in column_data:
                    value = value.strip()

                    if value.isdigit():
                        self.integers.append(int(value))
                    elif self.is_float(value):
                        self.floats.append(float(value))
                    else:
                        self.strings.append(value)

                return {
                    "strings": self.strings,
                    "floats": self.floats,
                    "integers": self.integers
                }

        except FileNotFoundError:
            print("Le fichier n'existe pas.")
            return {
                "strings": [],
                "floats": [],
                "integers": []
            }

    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False


