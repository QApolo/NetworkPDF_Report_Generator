import json
from datetime import date
from fpdf import FPDF

class PdfReport(FPDF):
	def __init__(self, filepath):
		FPDF.__init__(self)
		self.add_page()
		self.set_font('Arial', 'B', 16)
		self.cell(40, 10, 'Reporte Rendimiento')
		self.ln()
		self.filepath = filepath
		
	def createReport(self):
		self.output(self.filepath, 'F')
	def generateCover(self, datacover):
		datacover['date'] = str(date.today())
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
	def addInformationServer(self, dataInformation):
		self.set_font('Arial', 'B', 16)
		self.multi_cell(0, 5, "Informacion ", align = 'C')
		self.set_font('Arial', '', 12)
		for k, v in dataInformation.items():
			suffix = ""
			if k == "speed_download":
				suffix = "bits / sec"

			self.multi_cell(0, 5, "%s : %s %s" %(k, v, suffix))
		self.ln()
		
if __name__ == "__main__":
	pdf = PdfReport("./Reporte.pdf")
	with open('cover.json') as json_file:  
	    coverdata = json.load(json_file)
	pdf.generateCover(coverdata['coverdata'])
	
	#for name in files:
	#with open("../Information/information.json") as json_file:
	with open("../../Rendimiento/information.json") as json_file:
		infodata = json.load(json_file)	
	pdf.addInformationServer(infodata)
	
	pdf.createReport()


	
