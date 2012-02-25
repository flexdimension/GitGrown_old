import Qt 4.7

Rectangle {
    width: 100
    height: 50

    property alias text: label.text

    Image {
        anchors.fill: parent
        source: "images/button.svg"
    }

    Text { id: label
        anchors.centerIn: parent
        text: "text"
        color: "white"
    }

}
