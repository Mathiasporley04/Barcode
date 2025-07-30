# 🏷️ Barcode V1.0 - Generador de Códigos de Barras

## 📋 Descripción
Generador profesional de códigos de barras Code39 optimizado para impresoras térmicas HY Z18LW DECODER V1.3. Genera etiquetas PDF de 4cm x 3cm con adaptación automática de tamaño.

# Error principal a corregir: NO ENCUENTRA EL ESCRITORIO (solamente funciona localmente en el escritorio de mi notebook)



## ✨ Características
- ✅ **Etiquetas 4cm x 3cm** - Tamaño exacto para impresión
- ✅ **Code39 optimizado** - Compatible con HY Z18LW DECODER V1.3
- ✅ **Adaptación automática** - Se ajusta según longitud del código
- ✅ **Impresión térmica** - Barras gruesas y separadas
- ✅ **Conversión automática** - `-` → `/` para compatibilidad
- ✅ **Interfaz simple** - Solo lo esencial
- ✅ **Registro Excel** - Mantiene historial automáticamente

## 🚀 Instalación

### 1. Instalar Python
Asegúrate de tener Python 3.7+ instalado en tu sistema.

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el programa
```bash
python generador_codigos_gui.py
```

## 📖 Uso

### Interfaz Principal
1. **Nombre del artículo**: Ingresa el nombre del producto
2. **Código del artículo**: Ingresa el código (ej: F-423-4234)
3. **GENERAR ETIQUETA**: Crea el PDF con código de barras
4. **ABRIR CARPETA**: Ve los archivos generados

### Características del Código de Barras
- **Symbología**: Code39
- **Conversión**: `-` se convierte automáticamente a `/`
- **Adaptación**: Se ajusta automáticamente según longitud
- **Margen**: 0.1mm mínimo en cada lado
- **Altura**: 12mm fija

### Texto del Nombre
- **≤30 caracteres**: Una línea, fuente 7.15pt
- **>30 caracteres**: Dos líneas, fuente 4.5pt
- **División inteligente**: Por espacios, no corta palabras

## 📁 Estructura de Archivos
```
Barcode V1.0/
├── generador_codigos_gui.py    # Programa principal
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
└── Codigos de barras/         # Carpeta de salida (se crea automáticamente)
    ├── [archivos PDF generados]
    └── Registro codigo de barras.xlsx
```

## 🔧 Configuración
- **Carpeta destino**: `C:\Users\mathi\OneDrive\Escritorio\Codigos de barras`
- **Tamaño etiqueta**: 4cm x 3cm
- **Formato PDF**: Dimensiones exactas

## 📊 Registro Excel
El programa crea automáticamente un archivo Excel con:
- **Nombre**: Nombre del artículo
- **Código**: Código original
- **Código de Barras**: Código convertido (con `/`)

## 🎯 Compatibilidad
- **Impresoras**: HY Z18LW DECODER V1.3
- **Symbología**: Code39
- **Sistema**: Windows 10/11
- **Python**: 3.7+

## 🚨 Notas Importantes
- Los campos se limpian automáticamente después de cada generación
- Los archivos se guardan con nombres seguros (sin caracteres especiales)
- El programa maneja errores automáticamente
- Compatible con impresoras térmicas

## 📞 Soporte
Para problemas o consultas, revisa que:
1. Python esté instalado correctamente
2. Las dependencias estén instaladas
3. Tengas permisos de escritura en el escritorio

---
**Versión**: 1.0  
**Fecha**: Julio 2025  
**Compatibilidad**: HY Z18LW DECODER V1.3 