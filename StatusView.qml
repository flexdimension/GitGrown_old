import Qt 4.7

Rectangle { id: statusView
    width:400
    height:600

    color: "#DDDDDD"

    Rectangle {
        anchors.fill: parent
        anchors.margins: 10
        clip: true

        Column { id: statusController
            width: parent.width

            Rectangle { id: title
                width: parent.width
                height: 40
                Text {
                    text: "Status"
                }
            }
            PushButton {
                width: 80
                height: 30
                text: "Refresh"
                objectName: "refreshButton"
                onClicked : {
                    console.log("StatusView:" + "refresh push button clicked!!")
                }
            }

            PushButton {
                width: 80
                height: 30
                text: "Undo Commit"
                objectName: "undoCommit"
                onClicked : {
                    console.log("StatusView:" + "Undo Commit push button clicked!!")
                }
            }

            PushButton {
                width: 80
                height: 30
                text: "Commit"
                objectName: "commitButton"

                signal commitWithMessage(string msg)

                onClicked : {
                    commitWithMessage(commitMessage.text)
                    console.log("StatusView:" + "commit push button clicked!!")
                }
            }

            Rectangle {
                width: parent.width
                height: 60
                border.color: "black"
                TextEdit { id: commitMessage
                    objectName: "commitMessage"
                    anchors.fill: parent
                    anchors.margins: 3
                }
            }
        }

        Rectangle { id: statusConsole
            width: parent.width
            anchors.top: statusController.bottom
            height: 300
            border.color:"gray"


            Text {
                id: statusText
                text: gitStatus
            }
        }

        ListView { id:indexView
            anchors.top: statusConsole.bottom
            width: parent.width
            height: 300
            model: indexModel
            delegate: indexDelegate

            clip: true
            spacing: 2

            objectName: "indexStatus"

            signal stageFile(string path)
            signal unstageFile(string path)
            signal discardFile(string path)

            Rectangle {
                width: parent.width / 2
                height: parent.count * 22
                radius: 10
                color: "#FFFFAA"
                border.color: "#AAAA33"
                border.width: 2
                z: -10
            }


            Component { id: indexDelegate
                Rectangle {
                    x : 10
                    width: parent.width - 20
                    height: 20
                    border.width: 1
                    border.color: "gray"
                    color: "transparent"

                    Rectangle { id: modifedFileBox
                        x: 0
                        width: parent.width / 2
                        height: 20
                        //Show only if file is modified and staged
                        visible: type.indexOf("M") != -1 || type.indexOf("R") != -1
                        border.width: 1
                        radius: 8


                        Text {
                            x:0
                            text: path + ":" + type
                            color: "green"
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked : {
                                console.log('unstage ' + path)
                                indexView.unstageFile(path)
                            }
                        }

                    }

                    Rectangle { id: changedFileBox
                        x: parent.width / 2
                        width: parent.width / 2
                        height: 20
                        //Show only if the file is changed but not staged
                        visible: type.indexOf("C") != -1
                        border.width: 1
                        radius: 8

                        Text {
                            x:0
                            text: path + ":" + type
                            color: "red"
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked : {
                                console.log('stage ' + path)
                                indexView.stageFile(path)
                            }
                        }
                    }

                    Rectangle { id: newFileBox
                        x: 0
                        width: parent.width / 2
                        height: 20
                        //Show only if file is modified and staged
                        visible: type.indexOf("N") != -1
                        color: "#AADDAA"
                        border.width: 1
                        radius: 8

                        Text {
                            x:0
                            text: path + ":" + type
                            color: "green"
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked : {
                                console.log('unstage ' + path)
                                indexView.unstageFile(path)
                            }
                        }
                    }



                    Rectangle { id: untrackedFileBox
                        x: parent.width / 2
                        width: parent.width / 2
                        height: 20
                        //Show only if the file is untracked
                        visible: type.indexOf("U") != -1
                        color: "#DDAAAA"
                        border.width: 1
                        radius: 8

                        Text {
                            x:0
                            text: path + ":" + type
                            color: "red"
                        }
                        MouseArea {
                            anchors.fill: parent
                            onClicked : {
                                console.log('stage ' + path)
                                indexView.stageFile(path)
                            }
                        }
                    }

                }
            }
        }
    }
}
