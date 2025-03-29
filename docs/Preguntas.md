# Entregable

## ¿Cómo especificarías mejor el requerimiento? (Validación)

Para especificar mejor el requerimiento, debemos asegurarnos de que esté claramente definido y sea comprensible para todas las partes involucradas. Para esto:
- **Describir con detalle los casos de uso**: Los casos de uso deben ser detallados y reflejar las interacciones del usuario con el sistema.
- **Proveer ejemplos claros de entradas y salidas**: Esto ayudará a visualizar cómo debe funcionar el sistema en diferentes escenarios.
- **Definir criterios de aceptación claros**: Establecer qué condiciones deben cumplirse para que el sistema sea considerado funcional y cumpla con los requerimientos.
- **Evitar ambigüedades**: Los requerimientos deben ser específicos para evitar malentendidos y asegurar que todas las partes comprendan lo que se espera.

## ¿Cómo asegurarías que el programa cumpla el requerimiento? (Verificación)

La verificación es clave para asegurar que el sistema se construya correctamente según las especificaciones. Para garantizar que el programa cumpla con el requerimiento:
- **Pruebas unitarias e integradas**: Implementar pruebas unitarias para validar cada componente y pruebas integradas para verificar que los componentes trabajen bien en conjunto.
- **Revisiones de código frecuentes**: Realizar revisiones de código en equipo para detectar posibles errores y asegurar que el código cumple con las especificaciones.
- **Automatización de pruebas**: Establecer un conjunto de pruebas automatizadas que se ejecuten cada vez que se realicen cambios, garantizando que el sistema se mantenga funcional.

## Organización del Proyecto y Flujo de Trabajo

El proyecto está organizado utilizando **Gitflow**, una estrategia de ramificación que ayuda a gestionar el trabajo en equipo de manera eficiente. El flujo de trabajo se organiza de la siguiente manera:
- **Main**: Contiene la versión estable y lista para producción del proyecto.
- **Develop**: Contiene las últimas actualizaciones del proyecto, aún en desarrollo.
- **Feature branches**: Ramas dedicadas a desarrollar nuevas funcionalidades. Se crean a partir de la rama `develop` y se fusionan nuevamente una vez que la funcionalidad está terminada.
- **Release branches**: Preparación para nuevas versiones, donde se realiza la corrección de errores y ajustes finales antes de pasar a producción.
- **Hotfix branches**: Se utilizan para corregir errores críticos en la versión de producción sin interrumpir el trabajo en desarrollo.

El flujo de trabajo se basa en **pull requests**, donde cada miembro del equipo revisa los cambios antes de fusionarlos con la rama principal.

## Evidencia de Flujo de Trabajo y Configuraciones Realizadas

Para proporcionar evidencia del flujo de trabajo y las configuraciones realizadas, se incluirán:
- **Capturas de pantalla** del repositorio en GitHub mostrando las ramas activas y las pull requests abiertas.

## Problemas Encontrados y Cómo se Solucionaron

Durante el desarrollo, se presentaron varios problemas comunes:
- **Conflictos de ramas**: A veces se generaron conflictos al integrar nuevas funcionalidades. Para solucionarlos, se utilizó el comando `git rebase` para mantener las ramas actualizadas y evitar conflictos antes de la fusión.
- **Errores en las pruebas unitarias**: Algunos errores fueron detectados tarde en el proceso de desarrollo. Para resolver esto, se mejoraron las pruebas unitarias, asegurando que cubrieran más escenarios y permitieran detectar errores de forma temprana.

## Pruebas

### Estrategia de Pruebas
Para probar el sistema, se implementará una estrategia basada en ciclos de pruebas individuales y pruebas consolidadas en conjunto con un compañero. 
Las pruebas serán principalmente funcionales para verificar el correcto comportamiento del sistema. **No se realizarán pruebas cruzadas**, ya que, dado que las pruebas se desarrollan en conjunto en el segundo ciclo, no son necesarias.

### Preparación y Ejecución de Pruebas

#### Ciclo de Pruebas 1 (Primera ejecución de conjunto de pruebas)
1. **Preparar conjunto de pruebas de manera individual**: Cada miembro del equipo preparará sus pruebas de manera independiente, asegurándose de que cubran los casos de uso definidos.
2. **Ejecutar de manera individual sobre el programa**: Se ejecutarán las pruebas de manera individual para validar que cada parte del sistema funcione correctamente.

#### Ciclo de Pruebas 2 (Segunda ejecución de conjunto de pruebas)
1. **Consolidar con compañero un único conjunto de pruebas**: Después de la ejecución inicial, se consolidarán las pruebas realizadas por cada miembro del equipo en un único conjunto.
2. **Ejecutar en conjunto las pruebas consolidadas en el programa**: Se ejecutarán las pruebas consolidadas en el programa para asegurar que todas las funcionalidades estén correctamente integradas y que el sistema funcione como se espera.

