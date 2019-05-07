import json
from fpdf import FPDF

class PdfReport(FPDF):
	def __init__(self, filepath):
		self.position = 10
		FPDF.__init__(self)
		self.add_page()
		self.set_font('Arial', 'B', 16)
		self.cell(40, 10, 'Reporte Rendimiento')
		self.ln()
		self.filepath = filepath
		
	def createReport(self):
		self.output(self.filepath, 'F')
	def generateCover(self, datacover):
		self.set_font('Arial', '', 12)
		for k, v in datacover.items():
			if str(k) == 'names':
				#print("names:")
				self.set_font('Arial', 'B', 12)
				self.multi_cell(0, 5, "Integrantes: ", align = 'C')
				self.set_font('Arial', '', 12)
				for name in v:
					self.multi_cell(0, 5, " "*4 + name, align = 'C')
					print(" "*12 + name)
					self.ln()
			else:
				self.set_font('Arial', 'B', 12)
				self.multi_cell(0, 5, ""+str(k)+ " : "+str(v), align = 'C')
				self.set_font('Arial', '', 12)
				print(""+str(k)+ " : "+str(v))
				self.ln()
		self.add_page()
	def generateConclusions(self):
		print("conclusions")
	def newposition(self):
		self.position += 20
		return self.position 
	def addInformationServer(self, dataInformation):
		self.multi_cell(0, 5, str(dataInformation))
		self.ln()
		
if __name__ == "__main__":
	pdf = PdfReport("./output.pdf")
	with open('cover.json') as json_file:  
	    coverdata = json.load(json_file)
	pdf.generateCover(coverdata['coverdata'])

	with open("../Information/information.json") as json_file:
		infodata = json.load(json_file)	
	pdf.addInformationServer(infodata)

	pdf.createReport()


	
