from Handler import OSMHandler
import time
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #start_ref = 923905562
    #end_ref = 708414998
    #start_ref = (56.79075, 60.62358)
    #end_ref = (56.80640, 60.62104)

    #start_ref = (56.836756, 60.599309)
    #end_ref = (56.840753, 60.614750)

    #start_ref = (56.82737, 60.60176)
    #end_ref = (56.83814, 60.60405)

    #start_ref = (56.79704, 60.61045)
    #end_ref = (56.83961, 60.57205)
    start_ref = (55.63265, 37.65817)
    end_ref = (55.8468, 37.44116)


    # walk, scooter
    #mode = 'walk'
    mode = 'walk'
    file = 'Moscow_graph.osm.pbf'
    handler = OSMHandler(start_ref, end_ref, mode=mode, file=file)
    handler.handle()


    # потом тут строим кратчайший путь
    # пока по узлам, потом по норм координатам
