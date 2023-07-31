class websocket {
    constructor(url) {
        this.url = url
        this.instance = ''
        this.retryInterval = 10000
        this.initWs()
        this.instance.onopen = () => {
            this.status = true
        }
        // this.instance.onerror = () => {
        //     this.status = false
        //     setInterval(() => {
        //         this.reconnect()
        //     }, this.retryInterval)
        // }
    }
    initWs() {
        this.instance = new WebSocket(this.url)
    }
    reconnect() {
        setTimeout(() => {
            this.initWs()
        }, 100)
    }
    getInstance() {
        return this.instance
    }
}

const ws = new websocket('ws://127.0.0.1:7070/api/v1/ws')
export default ws
