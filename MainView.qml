import Qt 4.7

Rectangle { id: root
    objectName: "root"

    width: 1000
    height: 800

    signal commited
    signal commitUndone(string msg)


    BranchFlowView { id: bfView
        x: 0
        y: 0
        height: 600
    }

    StatusView{ id: statusView
        x: bfView.width
        y: 0
        height: 600
    }

    ConsoleView {
        x: 0
        y: statusView.height
        width: parent.width
        height: 200
    }
}
