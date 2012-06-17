import Qt 4.7

Rectangle { id: root
    objectName: "root"

    width: 1000
    height: 600

    signal commited
    signal commitUndone(string msg)

    BranchFlowView { id: bfView
        x:0
        y:0
        height: 400
    }

    StatusView{
        anchors.left: bfView.right
        height: bfView.height
    }

    ConsoleView {
        x: 0
        anchors.top: bfView.bottom
        width: parent.width
        height: 200
    }
}
