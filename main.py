import cv2





def defects_searching(filename):


    img = cv2.imread(filename) # Загружаю изображение из папки в проекте
    img = img[5:1495, 5:2995] # На изображении есть синий контур, который мешает корректно искать грани
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Так как изображение черное белое преобразовывать в оттекни серого не нужно
    edges = cv2.Canny(img, 50, 150) # Ищу грани


    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))   # Убираю пробелы в гранях
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Ищу контуры среди обнаруженных граней

    # Начинаю отсчет квадратов, треугольников и других фигур
    triangles = 0
    squares = 0
    another = 0

    # Проходим по каждому контуру
    for contour in contours:
        # Аппроксимация контура многоугольника
        approx = cv2.approxPolyDP(contour, 0.05 * cv2.arcLength(contour, True), True)


        if len(approx) == 3:  # Проверка на 3 вершины
            triangles += 1
            another += 1

            cv2.drawContours(img, [approx], 0, (0, 255, 0), 4)  #  Рисую контур на оригинальном изображении


        if len(approx) == 4 and cv2.contourArea(approx) > 2000 and cv2.isContourConvex(approx): #Проверка на 4 вершины и площадь прямоугольника
            squares += 1
            another += 1

            cv2.drawContours(img, [approx], 0, (0, 0, 255), 4)   #  Рисую контур на оригинальном изображении
        else:
            another += 1

    # Вывожу результат
    cv2.putText(img, f"Triangles: {triangles}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(img, f"Squares: {squares}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(img, f"Total defects: {another}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    # Изменяю размер изображения, чтобы не оно не открывалось на весь экран
    img = cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2))

    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


defects_searching("2022-07-16_132310_q20_t20.png")
#defects_searching("2022-07-16_132306_q20_t20.png")
#defects_searching("2022-07-16_132308_q20_t20.png")
