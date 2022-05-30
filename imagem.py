import os
import tkinter
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab

# melhoria:
#   criacao da Pasta
#   pontos invertidos (nao retangulo esperado)

class Imagem():

    def __init__(self, arquivo_imagem, diretorio_imagem=os.getcwd()):
        image_reference_lower_extension = lambda x: x + self.image_extension if x.find(".") == -1 else x.split(".")[0] + "." + x.split(".")[1].lower()
        self.arquivo = image_reference_lower_extension(arquivo_imagem)
        self.extensao = self.arquivo.split(".")[1]
        self.diretorio = diretorio_imagem
        print(self.arquivo, self.diretorio)
        self._valida_diretorio()
        self._valida_presenca_imagem_no_diretorio()

    def _valida_diretorio(self, diretorio=""):
        if diretorio == "":
            diretorio = self.diretorio

        if not os.path.isdir(diretorio):
            raise Exception("Pasta inexistente")

    def _valida_presenca_imagem_no_diretorio(self, arquivo_imagem="", diretorio=""):
        if arquivo_imagem == "":
            arquivo_imagem = self.arquivo

        if diretorio == "":
            diretorio = self.diretorio
        else:
            self._valida_diretorio(diretorio)

        lista_arquivos_diretorio = [arquivo.split(".")[0] + "." + arquivo.split(".")[1].lower() for arquivo in os.listdir(diretorio) if arquivo.find(".") != -1]
        if not any(arquivo == arquivo_imagem for arquivo in lista_arquivos_diretorio):
            raise Exception("Pasta sem a imagem informada")

    def valida_presenca_extensao_no_diretorio(self, diretorio="", extensao_desejada=""):
        if extensao_desejada == "":
            extensao_desejada = self.extensao
        else:
            extensao_desejada = extensao_desejada.replace(".", "")

        if diretorio == "":
            diretorio = self.diretorio
        else:
            self._valida_diretorio(diretorio)

        lista_arquivos_diretorio = [arquivo.split(".")[0] + "." + arquivo.split(".")[1].lower() for arquivo in os.listdir(diretorio) if arquivo.find(".") != -1]
        if not any(arquivo.split(".")[1] == extensao_desejada for arquivo in lista_arquivos_diretorio):
            raise Exception("Nenhum arquivo com a extensao desejada presente na pasta")

        return [arquivo for arquivo in lista_arquivos_diretorio if arquivo.split(".")[1] == extensao_desejada]

    def crop_retangular_usando_imagem_como_referencia(self, imagem_referencia=None, diretorio_iteracao="", diretorio_salvar=""):
        if imagem_referencia == None:
            imagem_referencia = self
        if diretorio_iteracao != "":
            self._valida_diretorio(diretorio=diretorio_iteracao)
        else:
            diretorio_iteracao = self.diretorio
        if diretorio_salvar == "":
            diretorio_salvar = os.path.join(diretorio_iteracao, "imagens_cortadas")
            i=0
            while os.path.exists(diretorio_salvar) == True:
                i += 1
                diretorio_salvar = diretorio_salvar + "_" + str(i)
            os.mkdir(diretorio_salvar)

        pontos_corte = self.pega_pontos_corte_retangular(imagem_referencia.diretorio, imagem_referencia.arquivo)

        lista_arquivos_iteracao = self.valida_presenca_extensao_no_diretorio(diretorio_iteracao, imagem_referencia.extensao)
        for arquivo in lista_arquivos_iteracao:
            nome_arquivo_salvar = arquivo.split(".")[0] + "_cortado." + arquivo.split(".")[1]
            self.crop(os.path.join(diretorio_iteracao, arquivo), coords=pontos_corte, saved_location=os.path.join(diretorio_salvar, nome_arquivo_salvar))

    def pega_pontos_corte_retangular(self, diretorio_imagem, arquivo_referencia):

        global x0, y0, x1, y1, incremento

        dir_original = os.getcwd()
        os.chdir(diretorio_imagem)

        window = tkinter.Tk(className="bla")
        image = Image.open(str(arquivo_referencia))
        canvas = tkinter.Canvas(window, width=image.size[0], height=image.size[1])
        canvas.pack()
        image_tk = ImageTk.PhotoImage(image)
        canvas.create_image(image.size[0]//2, image.size[1]//2, image=image_tk)
        incremento = 0

        def callback(event):
            global x0, y0, x1, y1, incremento # https://bit.ly/2HByHeE
            incremento += 1
            if incremento == 1:
                x0, y0 = event.x, event.y
            elif incremento == 2:
                x1, y1 = event.x, event.y
                window.destroy() # https://bit.ly/1wfcibt
            # print("clicked at: ", event.x, event.y)

        incremento = 0
        canvas.bind("<Button-1>", callback)
        tkinter.mainloop()

        os.chdir(dir_original)

        print("P1: ", x0, y0, "/ P2: ", x1, y1)
        return [x0, y0, x1, y1]

    def crop(self, image_path, coords, saved_location):
        """
        @param image_path: The path to the image to edit
        @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
        @param saved_location: Path to save the cropped image
        """
        image_obj = Image.open(image_path)
        cropped_image = image_obj.crop(coords)
        cropped_image.save(saved_location)
        # cropped_image.show()


def loop_screenshot():
    i = 0
    try:
        while True:
            resposta = input("Tirar ScreenShot? (Sim/Quit):")
            if resposta.lower() == "s":
                i += 1
                im = ImageGrab.grab()
                im.save('screenshot_' + str(i) + '.png')
            elif resposta.lower() == "q":
                break
            else:
                print("Entre S ou Q\n")
    except KeyboardInterrupt:
        print("fechar")
