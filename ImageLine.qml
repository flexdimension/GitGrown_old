import Qt 4.7

Item {
    property int x1 : x
    property int y1 : y

    property int x2 : 0
    property int y2 : 0

    //property int targetX : x2 - x1
    //property int targetY :

    property int length : Math.sqrt((x2-x1) * (x2-x1) + (y2-y1) * (y2-y1))
    property int thick : 5


    property int sign : y2 - y1 < 0 ? -1 : 1

    visible: length > 0

    rotation : sign * Math.acos((x2 - x1) / length) * 180 / Math.PI


    Image {
        source: "images/line.svg"
        x : 0
        y : - parent.thick / 2

        width : parent.length
        height : 5
        //rotation : 30
    }
}
