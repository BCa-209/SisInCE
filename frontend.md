# Frontend — Sistema de Consulta y Exportación

## 1. Descripción general

La página web tendrá como objetivo permitir al usuario realizar consultas a una base de datos mediante diferentes criterios de búsqueda. Los resultados obtenidos podrán visualizarse, copiarse como texto y posteriormente utilizarse para generar una plantilla gráfica editable que podrá ser exportada a PDF.

---

## 2. Sección de búsqueda

La interfaz contará con una sección denominada **"BÚSQUEDA"**, donde el usuario podrá seleccionar el criterio mediante el cual desea realizar la consulta.

### Opciones de búsqueda

- **Código**
    
- **DNI**
    
- **Apellidos y Nombres**
    
- **Facultad**
    
- **Escuela Profesional**
    
- **Año de ingreso**
    
- **Ciclo**
    

Al seleccionar una opción, se deberá mostrar dinámicamente debajo de ella el campo correspondiente para introducir el dato que se desea buscar.

### Consideraciones

- El campo deberá cambiar según el criterio seleccionado.
    
- **Año de ingreso** deberá permitir seleccionar o introducir un año.
    
- **Ciclo** podrá dejarse vacío, ya que será un dato opcional.
    
- Dependiendo de la opción seleccionada, algunos campos podrían ser de tipo texto, número o selección.
    
- Deberá existir un botón para ejecutar la consulta.
    

---

## 3. Sección "RESULTADOS"

Debajo de la sección de búsqueda se mostrará un apartado denominado:

# RESULTADOS

Esta sección presentará la información obtenida de la consulta realizada a la base de datos.

Los resultados deberán:

- Mostrar los datos de forma clara y ordenada.
    
- Permitir seleccionar y **copiar el contenido como texto**.
    
- Mantener una estructura visual organizada para facilitar su lectura.
    
- Mostrar un mensaje cuando no se encuentren resultados.
    
- Mostrar un indicador de carga mientras se realiza la consulta.
    

Ejemplo:

```text
RESULTADOS

Código: 202012345
DNI: 12345678
Apellidos y Nombres: Juan Pérez Quispe
Facultad: Facultad de Ingeniería
Escuela Profesional: Ingeniería de Sistemas
Año de ingreso: 2020
Ciclo: I
```

---

## 4. Botón "EXPORTAR"

Debajo de los resultados deberá existir un botón:

**[ EXPORTAR ]**

Al presionar este botón:

1. Se actualizará la página o se habilitará la sección correspondiente.
    
2. Se generará una representación gráfica utilizando los datos obtenidos de la consulta.
    
3. Los datos deberán colocarse automáticamente sobre una **plantilla de imagen proporcionada previamente**.
    
4. La plantilla generada deberá mostrarse en un apartado independiente.
    

---

## 5. Plantilla editable

La imagen generada a partir de la plantilla deberá poder ser **editada antes de su impresión/exportación**.

El usuario deberá poder modificar los elementos permitidos de la plantilla, por ejemplo:

- Texto.
    
- Posición de los datos.
    
- Tamaño de determinados elementos.
    
- Otros campos configurables según las características de la plantilla.
    

La información obtenida de la base de datos deberá insertarse automáticamente en las posiciones correspondientes de la plantilla.

### Ejemplo conceptual

```text
┌─────────────────────────────────────────┐
│                                         │
│          [ PLANTILLA PROPORCIONADA ]    │
│                                         │
│   Código: 202012345                     │
│   DNI: 12345678                          │
│   Nombres: Juan Pérez Quispe             │
│   Facultad: Ingeniería                   │
│   Escuela: Ingeniería de Sistemas        │
│   Ingreso: 2020 - VIII                   │
│                                         │
└─────────────────────────────────────────┘
```

La plantilla deberá visualizarse dentro de un área de edición, permitiendo realizar los ajustes necesarios antes de generar el archivo final.

---

## 6. Botón "IMPRIMIR"

Debajo del editor de la plantilla deberá existir un botón:

**[ IMPRIMIR ]**

Al presionarlo, el sistema deberá:

1. Tomar la plantilla con los datos ya colocados y editados.
    
2. Generar un archivo **PDF**.
    
3. Mantener las dimensiones y proporciones de la plantilla original.
    
4. Permitir al usuario descargar o imprimir el PDF generado.
    

---

## 7. Vista general del flujo

El flujo de la página será:

```text
┌──────────────────────────┐
│       BÚSQUEDA           │
├──────────────────────────┤
│ Criterio de búsqueda     │
│ [ Código             ▼ ] │
│                          │
│ Campo de búsqueda        │
│ [______________________] │
│                          │
│       [ BUSCAR ]         │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│       RESULTADOS          │
├──────────────────────────┤
│ Datos obtenidos de la     │
│ consulta a la base de     │
│ datos                     │
│                          │
│ [ Copiar como texto ]     │
│                          │
│       [ EXPORTAR ]        │
└────────────┬─────────────┘
             ↓
┌──────────────────────────┐
│    PLANTILLA EDITABLE     │
├──────────────────────────┤
│                          │
│  Imagen proporcionada    │
│  + datos de la consulta  │
│                          │
│  Área de edición         │
│                          │
└────────────┬─────────────┘
             ↓
        [ IMPRIMIR ]
             ↓
┌──────────────────────────┐
│      PDF GENERADO         │
│                          │
│   [ Descargar / Imprimir ]│
└──────────────────────────┘
```

## 8. Requisitos de interfaz

La interfaz deberá ser sencilla, clara y responsive, permitiendo utilizar el sistema tanto en computadora como en dispositivos móviles.

La página deberá organizarse principalmente en tres bloques:

1. **Búsqueda:** selección del criterio e ingreso de los datos.
    
2. **Resultados:** visualización y copia de la información obtenida.
    
3. **Exportación:** generación, edición e impresión de la plantilla.
    

Los botones **BUSCAR**, **EXPORTAR** e **IMPRIMIR** deberán ser claramente visibles y diferenciarse visualmente de los campos de información.