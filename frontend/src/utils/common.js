import webConfig from '@/global.config'

export function splitSkinId(skinId) {
    console.log(skinId)
    const championId = skinId.slice(0, -3)
    const skinNumber = parseInt(skinId.slice(-3)).toString()
    const championName = webConfig.champions[championId].alias
    return `${championName}_${skinNumber}`
}

export function diffDays(date) {
    const targetDate = new Date(date)
    const targetTimestamp = targetDate.getTime()
    // 获取当前日期的时间戳
    const currentTimestamp = Date.now()
    // 计算日期差（单位为毫秒）
    const diffTimestamp = currentTimestamp - targetTimestamp
    // 将日期差转换为天数
    const diffDays = Math.floor(diffTimestamp / (1000 * 60 * 60 * 24))
    return diffDays
}

export function formatDuration(duration) {
    const minutes = Math.floor(duration / 60)
    const seconds = Math.floor(duration % 60)
    return `${minutes}m ${seconds}s`
}

export function formatMMDD(dateStr) {
    const date = new Date(dateStr)
    const month = date.getUTCMonth() + 1 // 获取月份，注意需要加 1
    const day = date.getUTCDate() // 获取日期
    const formattedDate = `${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}` // 将月份和日期格式化为 mm-dd 形式
    return formattedDate
}

export function formatHHMM(dateStr) {
    const date = new Date(dateStr)
    const hour = date.getUTCHours()
    const minute = date.getUTCMinutes()
    const formattedDate = `${hour.toString().padStart(2, '0')}:${minute
        .toString()
        .padStart(2, '0')}`
    return formattedDate
}

export function copyText(text) {
    const textarea = document.createElement('textarea')
    textarea.value = text
    document.body.appendChild(textarea)
    textarea.select() // 在这里调用 select() 方法
    document.execCommand('copy')
    document.body.removeChild(textarea)
}

export function calculateKDA(kills, assists, deaths) {
    // 计算KDA
    let kda = (kills + assists) / (deaths + 1)

    // 将KDA映射到3.0到18.0之间
    let kdaRange = (18 - 3) / (1 + Math.exp(-0.2 * (kda - 3)))

    // 返回KDA值
    return kdaRange.toFixed(1)
}

export function formatNumber(num) {
    if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'k'
    }
    return num.toString()
}

export function scrollTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth', // 添加平滑滚动效果
    })
}

export function openExternel(url) {
    window.shell.openExternal(url)
}
