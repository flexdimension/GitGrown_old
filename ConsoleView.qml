import Qt 4.7

Rectangle { id: statusConsole
    width: 400
    height: 200
    border.color:"gray"


    Text {
        id: statusText
        text: gitStatus
    }
}
