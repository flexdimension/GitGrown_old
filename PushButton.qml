import Qt 4.7

Rectangle { id: pushButton
    width: 100
    height: 50

    property alias text: label.text

    signal clicked()

    Image {
        anchors.fill: parent
        source: "images/button.svg"
    }

    Text { id: label
        anchors.centerIn: parent
        text: "text"
        color: "white"
    }

    MouseArea { id: mouseArea
        anchors.fill: parent
        onClicked: pushButton.clicked()
    }
}
