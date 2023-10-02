# 8Pay-web
Código página web PAYMENT, LANDINGPAGE y DASHBOARD sistema 8 Pay
#  
#
## DOCUMENTACIÓN GIT
### Uso de Github
Para la estructuración y uso de *branches* se debe tomar en cuenta la siguiente [guía](https://cleventy.com/que-es-git-flow-y-como-funciona/).
#### Branch *main*
Contiene el codigo que se encuentra en modo *release* o *producción*.
El nombre del commit siempre debe ser según el siguiente formato: *v {nº versión}*. Ejemplo: *v 1.1*
Commit: solo el administrador del repositorio.
#### Branch *sandbox*
Contiene el codigo que se encuentra en *testeo*.
Commit: administrador del repositorio y encargados de testing.
#### Branch *developmen*
Contiene el codigo que se encuentra en *desarrollo*.
Commit: cualquiera que esté trabajando en el desarrollo de una *branch*.
#
***FLUJO***: development -> sandbox -> main.
#
### Nº versión
Para la versión del código se seguirá la siguiente estructura:
#### Formato y dígitos
Contará con hasta 3 números y mínimo 2, separados por un '.'.
#### Primer dígito
***-DESARROLLO***: Siempre será un *0*.
***-TESTEO***: Siempre será una *b*.
***-PRODUCCIÓN***: Representa el correlativo para el número de la versión del código.
#### Segundo dígito
***-DESARROLLO***: Corresponderá al número del correlativo de la versión de release al que apunta.
***-TESTEO***: Corresponderá a al dígito una vez esté en producción.
***-PRODUCCIÓN***: Representa el correlativo de las actualizaciones del codigo producto de mejoras.
#### Tercer dígito
***-DESARROLLO***: Corresponderá al número del correlativo de la actualicación de release al que apunta.
***-TESTEO***: Corresponderá a al dígito una vez esté en producción.
***-PRODUCCIÓN***: Representa el correlativo de las actualizaciones del codigo producto de errores.
#### Ejemplo
***-DESARROLLO***: *0.1.1*
***-TESTEO***: *b.1.1*
***-PRODUCCIÓN***: *1.1*  
->Si se debe actualizar para mejorar un error, el release quedará *1.1.1*
#
### Sugerencia
Se sugiere utilizar *GitHub Desktop* para el control y actualizacion del código en GitHub.
