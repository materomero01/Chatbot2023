city('HongKong').
city('Bangkok').
city('Londres').
city('Singapur').
city('Paris').
city('Dubai').
city('Nueva York').
city('Estambul').
city('Roma').
city('Tokio').
city('Miami').
city('Milan').
city('Las Vegas').
city('Barcelona').
city('Shanghai').
city('Amsterdam').
city('Viena').
city('Los Angeles').
city('Venecia').
city('Orlando').
city('Berlin').
city('Florencia').
city('Johannesburgo').
city('Madrid').
city('Dublin').
city('Moscu').
city('Beijing').
city('Atenas').
city('Budapest').
city('Cancun').
city('San Francisco').
city('Toronto').
city('Munich').
city('Punta Cana').
city('Sydney').
city('Bruselas').
city('Santiago').
city('Doha').
city('Lisboa').
city('El Cairo').
city('San Petersburgo').
city('Cracovia').
city('Lima').
city('Auckland').
city('Honolulu').
city('Ciudad de Mexico').
city('Vancouver').
city('Buenos Aires').
city('Melbourne').
city('Niza').
city('Bariloche').
city('Salta').
city('Jujuy').
city('Calafate').
city('Cataratas del Iguazu').
city('Ushuaia').
city('Necochea').
city('Frankfurt').
city('Washington DC').
city('Abu Dhabi').

pais('China','HongKong').
pais('Tailandia','Bangkok').
pais('Inglaterra','Londres').
pais('Singapur','Singapur').
pais('Francia','Paris').
pais('Emiratos Arabes Unidos','Dubai').
pais('Estados Unidos','Nueva York').
pais('Turquia','Estambul').
pais('Italia','Roma').
pais('Japon','Tokio').
pais('Estados Unidos','Miami').
pais('Italia','Milan').
pais('Estados Unidos','Las Vegas').
pais('Espana','Barcelona').
pais('China','Shanghai').
pais('Paises Bajos','Amsterdam').
pais('Austria','Viena').
pais('Estados Unidos','Los Angeles').
pais('Italia','Venecia').
pais('Estados Unidos','Orlando').
pais('Alemania','Berlin').
pais('Italia','Florencia').
pais('Sudafrica','Johannesburgo').
pais('Espana','Madrid').
pais('Irlanda','Dublin').
pais('Rusia','Moscu').
pais('China','Beijing').
pais('Grecia','Atenas').
pais('Hungria','Budapest').
pais('Mexico','Cancun').
pais('Estados Unidos','San Francisco').
pais('Canada','Toronto').
pais('Alemania','Munich').
pais('Republica Dominicana','Punta Cana').
pais('Australia','Sydney').
pais('Belgica','Bruselas').
pais('Chile','Santiago').
pais('Qatar','Doha').
pais('Portugal','Lisboa').
pais('Egipto','El Cairo').
pais('Rusia','San Petersburgo').
pais('Polonia','Cracovia').
pais('Peru','Lima').
pais('Nueva Zelanda','Auckland').
pais('Estados Unidos','Honolulu').
pais('Mexico','Ciudad de Mexico').
pais('Canada','Vancouver').
pais('Argentina','Buenos Aires').
pais('Australia','Melbourne').
pais('Francia','Niza').
pais('Alemania','Frankfurt').
pais('Estados Unidos','Washington DC').
pais('Emiratos Arabes Unidos','Abu Dhabi').
pais('Argentina','Bariloche').
pais('Argentina','Salta').
pais('Argentina','Jujuy').
pais('Argentina','Calafate').
pais('Argentina','Peninsula de Valdes').
pais('Argentina','Ushuaia').
pais('Argentina','Necochea').

tiene('Hong Kong', 'ciudad').
tiene('Bangkok', 'ciudad').
tiene('Londres', 'ciudad').
tiene('Singapur', 'ciudad').
tiene('Paris', 'ciudad').
tiene('Dubai', 'ciudad').
tiene('Nueva York', 'ciudad').
tiene('Estambul', 'ciudad').
tiene('Roma', 'ciudad').
tiene('Tokio', 'ciudad').
tiene('Miami', 'playa').
tiene('Milan', 'ciudad').
tiene('Las Vegas', 'ciudad').
tiene('Barcelona', 'ciudad').
tiene('Shanghai', 'ciudad').
tiene('Amsterdam', 'ciudad').
tiene('Viena', 'ciudad').
tiene('Los Angeles', 'ciudad').
tiene('Venecia', 'ciudad').
tiene('Orlando', 'ciudad').
tiene('Berlin', 'ciudad').
tiene('Florencia', 'ciudad').
tiene('Johannesburgo', 'ciudad').
tiene('Madrid', 'ciudad').
tiene('Dublin', 'ciudad').
tiene('Moscu', 'ciudad').
tiene('Beijing', 'ciudad').
tiene('Atenas', 'ciudad').
tiene('Budapest', 'ciudad').
tiene('Cancun', 'playa').
tiene('San Francisco', 'ciudad').
tiene('Toronto', 'ciudad').
tiene('Munich', 'ciudad').
tiene('Punta Cana', 'playa').
tiene('Sydney', 'ciudad').
tiene('Bruselas', 'ciudad').
tiene('Santiago', 'ciudad').
tiene('Doha', 'ciudad').
tiene('Lisboa', 'ciudad').
tiene('El Cairo', 'ciudad').
tiene('San Petersburgo', 'ciudad').
tiene('Cracovia', 'ciudad').
tiene('Lima', 'playa').
tiene('Auckland', 'ciudad').
tiene('Honolulu', 'playa').
tiene('Ciudad de Mexico', 'ciudad').
tiene('Vancouver', 'ciudad').
tiene('Buenos Aires', 'ciudad').
tiene('Melbourne', 'ciudad').
tiene('Niza', 'playa').
tiene('Frankfurt', 'ciudad').
tiene('Washington DC', 'ciudad').
tiene('Abu Dhabi', 'playa').
tiene('Bariloche', 'montana').
tiene('Salta', 'montana').
tiene('Jujuy', 'montana').
tiene('Calafate', 'montana').
tiene('Cataratas del Iguazu', 'ciudad').
tiene('Ushuaia', 'montana').
tiene('Necochea', 'playa').


hotel('Barcelo').
hotel('Riu').
hotel('Iberostar').
hotel('Marriott').
hotel('Hilton').
hotel('Wyndham').
hotel('Hyatt').
hotel('IHG').
hotel('Accor').
hotel('Huazhu').
hotel('Melia').
hotel('Jin Jiang').
hotel('InterContinental').
hotel('Best Western').
hotel('Radisson').

mostrar_hoteles(Hoteles) :- 
    findall(Hotel, hotel(Hotel), Hoteles).

atraccion('playa').
atraccion('montana').
atraccion('ciudad').

paquete(Nombre, Destinos) :- 
    atom(Nombre), 
    is_list(Destinos).

paquete('Caribe', ['Punta Cana', 'Cancun']).
paquete('Disney', ['Miami', 'Orlando']).
paquete('Sur argentino', ['Bariloche', 'Calafate', 'Ushuaia']).
paquete('Mejor playa argentina', ['Necochea']).
paquete('Europa', ['Madrid', 'Atenas', 'Berlin', 'Venecia']).
paquete('Asia', ['Beijing', 'Japon', 'Hong Kong']).


esta_en(Atraccion, Ciudad) :- tiene(Ciudad, Atraccion).

mostrar_city(Cities) :-
    findall(City, city(City),Cities).

ciudad_pais(Pais, Ciudades) :-
     findall(Ciudad, pais(Pais, Ciudad),Ciudades).

tiene_ciudad(Atraccion, Ciudades) :-
     findall(Ciudad, esta_en(Atraccion, Ciudad),Ciudades).

ciudad_tiene(Ciudades,Atracciones) :-
     findall(Atraccion, tiene(Ciudades,Atraccion),Atracciones).















