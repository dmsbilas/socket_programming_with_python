import Foundation

let serverIP = "127.0.0.1"
let serverPort: UInt16 = 65432
let bufferSize = 4096

func createSocket() -> Int32? {
    let sock = socket(AF_INET, SOCK_STREAM, 0)
    guard sock >= 0 else {
        print("Failed to create socket")
        return nil
    }
    
    var serverAddr = sockaddr_in()
    serverAddr.sin_family = sa_family_t(AF_INET)
    serverAddr.sin_port = in_port_t(serverPort).bigEndian
    inet_pton(AF_INET, serverIP, &serverAddr.sin_addr)

    let connectResult = withUnsafePointer(to: &serverAddr) {
        $0.withMemoryRebound(to: sockaddr.self, capacity: 1) {
            connect(sock, $0, socklen_t(MemoryLayout<sockaddr_in>.size))
        }
    }

    guard connectResult == 0 else {
        print("Connection failed")
        close(sock)
        return nil
    }

    return sock
}

func uploadFile(filename: String) {
    let sourcePath = "./image_source/\(filename)"
    guard FileManager.default.fileExists(atPath: sourcePath),
          let fileHandle = FileHandle(forReadingAtPath: sourcePath),
          let sock = createSocket() else {
        print("File does not exist or socket error")
        return
    }

    let command = "UPLOAD \(filename)"
    send(sock, command, command.count, 0)

    while true {
        let data = fileHandle.readData(ofLength: bufferSize)
        if data.isEmpty { break }
        _ = data.withUnsafeBytes {
            send(sock, $0.baseAddress!, data.count, 0)
        }
    }

    fileHandle.closeFile()
    close(sock)
    print("Uploaded \(filename) successfully.")
}

func downloadFile(filename: String) {
    let destinationPath = "./download/\(filename)"
    guard let sock = createSocket() else { return }

    let command = "DOWNLOAD \(filename)"
    send(sock, command, command.count, 0)

    FileManager.default.createFile(atPath: destinationPath, contents: nil, attributes: nil)
    guard let fileHandle = FileHandle(forWritingAtPath: destinationPath) else {
        print("Could not create destination file")
        return
    }

    var buffer = [UInt8](repeating: 0, count: bufferSize)
    while true {
        let received = recv(sock, &buffer, bufferSize, 0)
        if received <= 0 { break }
        fileHandle.write(Data(bytes: buffer, count: received))
    }

    fileHandle.closeFile()
    close(sock)
    print("Downloaded \(filename).")
}

// Main
uploadFile(filename: "1.jpg")
downloadFile(filename: "1.jpg")
