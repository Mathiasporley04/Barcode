import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.graphics.barcode import code39
import threading
import webbrowser

class GeneradorCodigosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Códigos de Barras - HY Z18LW")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.carpeta_destino = ""
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Inicializar carpeta
        self.inicializar_carpeta()
    
    def configurar_estilo(self):
        """Configura el estilo de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), foreground='#2c3e50')
        style.configure('Title.TLabel', font=('Segoe UI', 12, 'bold'), foreground='#34495e')
        
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título principal
        titulo = ttk.Label(main_frame, text="🏷️ GENERADOR DE CÓDIGOS DE BARRAS", 
                          style='Header.TLabel')
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Subtítulo
        subtitulo = ttk.Label(main_frame, text="Etiquetas 4cm x 3cm - Compatible HY Z18LW DECODER V1.3", 
                             style='Title.TLabel')
        subtitulo.grid(row=1, column=0, columnspan=3, pady=(0, 30))
        
        # Frame de información
        info_frame = ttk.LabelFrame(main_frame, text="📋 Información del Sistema", padding="15")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        info_frame.columnconfigure(1, weight=1)
        
        # Información del sistema
        ttk.Label(info_frame, text="📁 Carpeta de destino:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.label_carpeta = ttk.Label(info_frame, text="No configurada", foreground='#e74c3c')
        self.label_carpeta.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(info_frame, text="📏 Tamaño de etiqueta:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(info_frame, text="4cm x 3cm", font=('Segoe UI', 10, 'bold')).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Frame de entrada de datos
        datos_frame = ttk.LabelFrame(main_frame, text="📝 Datos del Artículo", padding="15")
        datos_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        datos_frame.columnconfigure(1, weight=1)
        
        # Nombre del artículo
        ttk.Label(datos_frame, text="📦 Nombre del artículo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(datos_frame, font=('Segoe UI', 10))
        self.entry_nombre.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.entry_nombre.focus()
        
        # Código del artículo
        ttk.Label(datos_frame, text="🔢 Código del artículo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_codigo = ttk.Entry(datos_frame, font=('Segoe UI', 10))
        self.entry_codigo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Frame de botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=4, column=0, columnspan=3, pady=(0, 20))
        
        # Botón generar
        self.btn_generar = ttk.Button(botones_frame, text="🚀 GENERAR ETIQUETA", 
                                     command=self.generar_etiqueta, style='TButton')
        self.btn_generar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón abrir carpeta
        self.btn_abrir_carpeta = ttk.Button(botones_frame, text="📁 ABRIR CARPETA", 
                                            command=self.abrir_carpeta)
        self.btn_abrir_carpeta.pack(side=tk.LEFT)
        
        # Configurar eventos
        self.entry_nombre.bind('<Return>', lambda e: self.entry_codigo.focus())
        self.entry_codigo.bind('<Return>', lambda e: self.generar_etiqueta())
    
    def inicializar_carpeta(self):
        """Inicializa la carpeta de destino"""
        try:
            escritorio = r"C:\Users\mathi\OneDrive\Escritorio"
            self.carpeta_destino = os.path.join(escritorio, "Codigos de barras")
            
            if not os.path.exists(self.carpeta_destino):
                os.makedirs(self.carpeta_destino)
            
            self.label_carpeta.config(text=self.carpeta_destino, foreground='#27ae60')
            
        except Exception as e:
            self.label_carpeta.config(text="Error", foreground='#e74c3c')
    

    
    def limpiar_campos(self):
        """Limpia los campos de entrada"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.focus()
    
    def generar_etiqueta(self):
        """Genera la etiqueta en un hilo separado"""
        nombre = self.entry_nombre.get().strip()
        codigo = self.entry_codigo.get().strip()
        
        if not nombre:
            messagebox.showerror("Error", "❌ El nombre del artículo es obligatorio")
            self.entry_nombre.focus()
            return
        
        if not codigo:
            messagebox.showerror("Error", "❌ El código del artículo es obligatorio")
            self.entry_codigo.focus()
            return
        
        # Deshabilitar botón
        self.btn_generar.config(state='disabled')
        
        # Ejecutar en hilo separado
        thread = threading.Thread(target=self._generar_etiqueta_thread, args=(nombre, codigo))
        thread.daemon = True
        thread.start()
    
    def _generar_etiqueta_thread(self, nombre, codigo):
        """Genera la etiqueta en un hilo separado"""
        try:
            ruta_pdf = self.generar_pdf_con_codigo_profesional(nombre, codigo)
            
            if ruta_pdf:
                self.actualizar_excel(nombre, codigo, ruta_pdf)
                
                # Actualizar UI en el hilo principal
                self.root.after(0, self._etiqueta_generada_exitosa, ruta_pdf)
            else:
                self.root.after(0, self._etiqueta_generada_error)
                
        except Exception as e:
            self.root.after(0, lambda: self._mostrar_error(f"Error generando etiqueta: {e}"))
    
    def _etiqueta_generada_exitosa(self, ruta_pdf):
        """Maneja la generación exitosa de la etiqueta"""
        self.btn_generar.config(state='normal')
        
        mensaje = f"✅ ¡ETIQUETA GENERADA!\n\n"
        mensaje += f"📄 Archivo: {os.path.basename(ruta_pdf)}\n"
        mensaje += f"📏 Tamaño: 4cm x 3cm\n"
        mensaje += f"🔄 Conversión aplicada: - → /\n"
        mensaje += f"📁 Ubicación: {self.carpeta_destino}"
        
        messagebox.showinfo("Éxito", mensaje)
        
        # Limpiar campos para la siguiente etiqueta
        self.limpiar_campos()
    
    def _etiqueta_generada_error(self):
        """Maneja el error en la generación de la etiqueta"""
        self.btn_generar.config(state='normal')
        messagebox.showerror("Error", "❌ No se pudo generar la etiqueta")
    
    def _mostrar_error(self, mensaje):
        """Muestra un mensaje de error"""
        self.btn_generar.config(state='normal')
        messagebox.showerror("Error", mensaje)
    
    def abrir_carpeta(self):
        """Abre la carpeta de destino"""
        if self.carpeta_destino and os.path.exists(self.carpeta_destino):
            try:
                os.startfile(self.carpeta_destino)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la carpeta: {e}")
        else:
            messagebox.showerror("Error", "La carpeta de destino no existe")
    
    def limpiar_nombre_archivo(self, texto):
        """Limpia el texto para usar como nombre de archivo"""
        caracteres_prohibidos = '<>:"/\\|?*'
        texto_limpio = str(texto)
        
        for char in caracteres_prohibidos:
            texto_limpio = texto_limpio.replace(char, '_')
        
        if len(texto_limpio) > 50:
            texto_limpio = texto_limpio[:50]
        
        return texto_limpio
    
    def convertir_para_code39_hy_z18lw(self, codigo):
        """Convierte el código para que se lea correctamente en HY Z18LW DECODER V1.3 con Code39 optimizado"""
        codigo_original = str(codigo).upper()
        codigo_para_barcode = codigo_original.replace("-", "/")
        
        # Code39 soporta letras, números y algunos símbolos
        # Remover caracteres problemáticos
        caracteres_problematicos = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05', '\x06', '\x07', 
                                   '\x08', '\x09', '\x0A', '\x0B', '\x0C', '\x0D', '\x0E', '\x0F',
                                   '\x10', '\x11', '\x12', '\x13', '\x14', '\x15', '\x16', '\x17',
                                   '\x18', '\x19', '\x1A', '\x1B', '\x1C', '\x1D', '\x1E', '\x1F']
        
        codigo_limpio = ""
        for char in codigo_para_barcode:
            if char not in caracteres_problematicos:
                codigo_limpio += char
        
        # Si el código quedó vacío, usar el original
        if not codigo_limpio.strip():
            codigo_limpio = codigo_original.replace("-", "/")
        
        return codigo_limpio
    
    def generar_pdf_con_codigo_profesional(self, nombre_articulo, codigo):
        """Genera PDF con código de barras Code39 optimizado para impresoras térmicas en formato etiqueta 4cm x 3cm"""
        try:
            nombre_archivo = f"{self.limpiar_nombre_archivo(nombre_articulo)}_{self.limpiar_nombre_archivo(codigo)}.pdf"
            ruta_pdf = os.path.join(self.carpeta_destino, nombre_archivo)
            
            # CONVERSIÓN ESPECÍFICA PARA HY Z18LW DECODER V1.3 CON CODE39
            codigo_para_barcode = self.convertir_para_code39_hy_z18lw(codigo)
            
            if not codigo_para_barcode:
                return None
            
            # DIMENSIONES DE ETIQUETA 4cm x 3cm
            etiqueta_width = 4*cm
            etiqueta_height = 3*cm
            
            # Crear el PDF con dimensiones exactas de etiqueta
            c = canvas.Canvas(ruta_pdf, pagesize=(etiqueta_width, etiqueta_height))
            
            # LAYOUT OPTIMIZADO PARA ETIQUETA PEQUEÑA - CENTRADO PERFECTO
            
            # CÓDIGO DE BARRAS (CENTRO PERFECTO) - Centrado verticalmente
            # Posición Y del código de barras: centrado en los 3cm disponibles
            y_barcode_center = etiqueta_height / 2
            
            # Crear Code39 optimizado para impresoras térmicas con adaptación automática
            margen_barra = 0.1*mm  # Margen prácticamente cero
            max_width = etiqueta_width - 2*margen_barra  # Ancho máximo disponible
            
            # Configuraciones de barcode de mayor a menor tamaño
            configuraciones = [
                {'barWidth': 0.8*mm, 'gap': 1.2*mm},  # Configuración ideal
                {'barWidth': 0.6*mm, 'gap': 1.0*mm},  # Configuración media
                {'barWidth': 0.4*mm, 'gap': 0.8*mm},  # Configuración pequeña
                {'barWidth': 0.3*mm, 'gap': 0.6*mm},  # Configuración muy pequeña
                {'barWidth': 0.2*mm, 'gap': 0.4*mm},  # Configuración mínima
            ]
            
            barcode = None
            for config in configuraciones:
                try:
                    barcode = code39.Standard39(
                        codigo_para_barcode,
                        barHeight=12*mm,  # Altura del código de barras
                        barWidth=config['barWidth'],
                        humanReadable=False,
                        checksum=False,
                        gap=config['gap']
                    )
                    
                    # Si el barcode cabe en el espacio disponible, usar esta configuración
                    if barcode.width <= max_width:
                        break
                        
                except Exception as barcode_error:
                    continue
            
            # Si ninguna configuración funcionó, usar la más pequeña posible
            if barcode is None:
                try:
                    barcode = code39.Standard39(
                        codigo_para_barcode,
                        barHeight=12*mm,
                        barWidth=0.15*mm,  # Barras muy finas
                        humanReadable=False,
                        checksum=False,
                        gap=0.3*mm  # Espaciado mínimo
                    )
                except Exception as barcode_error:
                    return None
            
            # Centrar el código de barras con margen prácticamente cero
            margen_simple = 0.1*mm  # Margen prácticamente cero
            x_barcode = (etiqueta_width - barcode.width) / 2
            y_barcode = y_barcode_center - (barcode.height / 2)
            
            # Dibujar el código de barras
            barcode.drawOn(c, x_barcode, y_barcode)
            
            # NOMBRE DEL ARTÍCULO (ARRIBA) - División en carácter 30 con reducción 10%
            y_nombre = etiqueta_height - 6*mm  # Posición más cercana al código de barras
            
            # Lógica de división del texto
            if len(nombre_articulo) <= 30:
                # Si tiene 30 caracteres o menos, usar una línea vacía para espaciado correcto
                lineas = ["", nombre_articulo]  # Una línea vacía para espaciado correcto
                font_size_final = 7.15
                y_nombre += etiqueta_height * 0.025  # Sube el texto un 10% hacia arriba
            else:
                # Si pasa de 30 caracteres, dividir de manera inteligente por espacios
                # Buscar el mejor punto de división cerca de la mitad
                mitad = len(nombre_articulo) // 2
                mejor_corte = mitad
                
                # Buscar el espacio más cercano a la mitad (hacia atrás primero)
                for i in range(mitad, max(0, mitad - 15), -1):
                    if nombre_articulo[i] == ' ':
                        mejor_corte = i
                        break
                
                # Si no encontramos hacia atrás, buscar hacia adelante
                if mejor_corte == mitad:
                    for i in range(mitad, min(len(nombre_articulo), mitad + 15)):
                        if nombre_articulo[i] == ' ':
                            mejor_corte = i
                            break
                
                # Si aún no encontramos espacio, usar división por palabras
                if mejor_corte == mitad:
                    palabras = nombre_articulo.split()
                    if len(palabras) >= 2:
                        mitad_palabras = len(palabras) // 2
                        linea1 = ' '.join(palabras[:mitad_palabras])
                        linea2 = ' '.join(palabras[mitad_palabras:])
                    else:
                        # Si es una sola palabra, dividir en la mitad
                        linea1 = nombre_articulo[:mitad]
                        linea2 = nombre_articulo[mitad:]
                else:
                    # Usar el punto de corte encontrado
                    linea1 = nombre_articulo[:mejor_corte].strip()
                    linea2 = nombre_articulo[mejor_corte:].strip()
                
                # Verificar que ambas líneas tengan contenido
                if not linea1.strip():
                    linea1 = nombre_articulo[:10] + "..."
                    linea2 = nombre_articulo[10:]
                elif not linea2.strip():
                    linea1 = nombre_articulo[:-10] + "..."
                    linea2 = nombre_articulo[-10:]
                
                lineas = [linea1, linea2]
                font_size_final = 4.5  # Tamaño pequeño para textos largos
            
            # Calcular altura total del nombre
            altura_nombre = len(lineas) * (font_size_final + 0.2)  # Espaciado compacto
            espacio_disponible = y_nombre - y_barcode - 1*mm  # Margen pequeño
            
            # Verificar que ambas líneas quepan arriba del código de barras
            if altura_nombre > espacio_disponible:
                # Si no cabe, reducir más el tamaño
                while altura_nombre > espacio_disponible and font_size_final > 2.5:
                    font_size_final -= 0.1
                    altura_nombre = len(lineas) * (font_size_final + 0.2)
            
            # Dibujar las líneas del nombre (TODAS arriba del barcode)
            c.setFont("Helvetica-Bold", font_size_final)
            for i, linea in enumerate(lineas):
                linea_width = c.stringWidth(linea, "Helvetica-Bold", font_size_final)
                y_pos = y_nombre - (i * (font_size_final + 0.2))  # Espaciado compacto
                c.drawString((etiqueta_width - linea_width) / 2, y_pos, linea)
            
            # CÓDIGO NUMÉRICO (ABAJO) - Más cerca del código de barras
            y_codigo = y_barcode - 2*mm  # Posición relativa al código de barras (más cerca)
            c.setFont("Helvetica-Bold", 6)
            codigo_width = c.stringWidth(codigo, "Helvetica-Bold", 6)
            c.drawString((etiqueta_width - codigo_width) / 2, y_codigo, codigo)
            
            c.save()
            
            if os.path.exists(ruta_pdf):
                return ruta_pdf
            else:
                return None
                
        except Exception as e:
            return None
    
    def actualizar_excel(self, nombre_articulo, codigo, ruta_pdf):
        """Actualiza el registro en Excel con solo 3 columnas"""
        try:
            archivo_excel = os.path.join(self.carpeta_destino, "Registro codigo de barras.xlsx")
            
            nuevo_registro = {
                'Nombre': nombre_articulo,
                'Codigo': codigo,
                'Codigo de Barras': codigo.replace('-', '/')  # Código convertido para barcode
            }
            
            if os.path.exists(archivo_excel):
                try:
                    df = pd.read_excel(archivo_excel)
                    df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
                except:
                    df = pd.DataFrame([nuevo_registro])
            else:
                df = pd.DataFrame([nuevo_registro])
            
            df.to_excel(archivo_excel, index=False)
            
        except Exception as e:
            pass  # Silenciar errores de Excel

def main():
    """Función principal"""
    root = tk.Tk()
    app = GeneradorCodigosGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 