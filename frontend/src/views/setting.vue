<template>
    <div class="w-full h-full flex flex-col overflow-y-auto py-3 non-scrollbar">
        <div class="w-full flex-1 flex justify-center">
            <div class="w-full max-w-[1600px] flex">
                <div class="w-1/4 p-3">
                    <div class="card w-full rounded">
                        <div class="text-center py-8">
                            <div class="flex justify-center pb-8">
                                <img
                                    src="/src/assets/imgs/author.png"
                                    class="rounded-full elevation w-32"
                                />
                            </div>
                            <div class="font-bold tracking-wider text-xl">
                                {{ useGlobal.summoner.displayName }}
                            </div>
                            <div class="text-sm text-gray-500">艾欧尼亚</div>
                        </div>
                        <hr />
                        <div class="w-full h-16 flex items-center justify-center">
                            <span class="text-[15px] text-gray-500"
                                >当前版本号: {{ webConfig.version }}</span
                            >
                        </div>

                        <hr />
                        <div class="w-full h-16 flex items-center justify-center">
                            <span
                                class="text-[15px] text-gray-500"
                                @click="openExternel('http://github.com/XilyFeAAAA')"
                                >BiliBili: {{ webConfig.author }}</span
                            >
                        </div>
                    </div>
                </div>
                <div class="w-3/4 p-3">
                    <template v-if="settings">
                        <div class="card w-full rounded flex flex-col overflow-hidden">
                            <div
                                class="h-20 px-8 flex items-center cursor-pointer"
                                @click="show1 = !show1"
                            >
                                <span class="font-bold text-xl">常用功能</span>
                            </div>
                            <hr />

                            <collapse-transition>
                                <div class="px-6" v-show="show1">
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动举报队友</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    当对局失败时举报对内评分最低召唤师，无论游戏客户端是否处于前台都将执行此操作
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autoreport"
                                                v-model:checked="settings.autoReport"
                                            />
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动接受对局</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    当匹配到对局时将自动接受，无论游戏客户端是否处于前台都将执行此操作
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autoaccept"
                                                v-model:checked="settings.autoAccept.enable"
                                            />
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动配置符文</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在英雄选择阶段确定英雄时，将自动查询○PGG最佳符文数据并自动应用
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autorune"
                                                v-model:checked="settings.autoUseRune"
                                            />
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动重连游戏</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    当游戏异常退出时自动重新连接
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autoreconnect"
                                                v-model:checked="settings.autoReconnect"
                                            />
                                        </div>
                                    </div>
                                    <hr />

                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">段位伪造</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在上方选择需要修改的段位，好友可见
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-select
                                                collapse-tags
                                                default-first-option
                                                placeholder="请选择段位"
                                                v-model="el_rank"
                                                @change="onRankChange"
                                            >
                                                <el-option
                                                    v-for="item in rank_options"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value"
                                                >
                                                </el-option>
                                            </el-select>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">游戏状态修改</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在上方选择需要修改的状态，游戏客户端在线状态即可更改，好友可见
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-select
                                                collapse-tags
                                                default-first-option
                                                placeholder="请选择状态"
                                                v-model="el_status"
                                                @change="onStatusChange"
                                            >
                                                <el-option
                                                    v-for="item in status_options"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value"
                                                >
                                                </el-option>
                                            </el-select>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">游戏名修改</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在上方输入需要修改的游戏名，仅自己可见，不包括生涯
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-input v-model="el_name" placeholder="">
                                                <template #append>
                                                    <span
                                                        @click="onNameChange"
                                                        class="cursor-pointer"
                                                        >修改</span
                                                    >
                                                </template>
                                            </el-input>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">签名修改</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在上方输入需要修改的签名
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-input v-model="el_sign" placeholder="">
                                                <template #append
                                                    ><span
                                                        @click="onSignChange"
                                                        class="cursor-pointer"
                                                        >修改</span
                                                    ></template
                                                >
                                            </el-input>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">5V5训练模式</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    点击按钮即可创建5v5训练模式房间，可添加9个机器人
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="onCreateLobby">
                                                <span class="text-sm text-gray-500">创建房间</span>
                                            </el-button>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">召唤师图标修改</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    该功能可以修改客户端的显示头像，但生涯以及列队界面大概率会变成默认头像点击此处查看头像素材
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="iconVisible = true">
                                                <span class="text-sm text-gray-500">选择图标</span>
                                            </el-button>
                                            <el-dialog v-model="iconVisible" title="选择你的图标">
                                                <div
                                                    class="w-full h-[400px] flex flex-wrap overflow-y-auto"
                                                >
                                                    <VlazyImage
                                                        v-for="id in webConfig.profileIcons"
                                                        width="100"
                                                        class="m-2 cursor-pointer"
                                                        :key="id"
                                                        :src="
                                                            'http://ddragon.leagueoflegends.com/cdn/13.14.1/img/profileicon/' +
                                                            id +
                                                            '.png'
                                                        "
                                                        @click="onProfileIconChange(id)"
                                                    />
                                                </div>
                                            </el-dialog>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">生涯背景修改</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    请选择需要修改的生涯图片，即可在游戏客户端中生效，可改所有生涯图片且所有人可见
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="bgVisible = true">
                                                <span class="text-sm text-gray-500">选择背景</span>
                                            </el-button>
                                            <el-dialog v-model="bgVisible" title="选择你的背景">
                                                <div class="w-full h-[400px]">
                                                    <div
                                                        class="w-full h-3/4 py-3 flex justify-center items-center"
                                                    >
                                                        <img
                                                            v-if="el_bgSkin"
                                                            class="h-full"
                                                            :src="`https://game.gtimg.cn/images/lol/act/img/skin/big${el_bgSkin}.jpg`"
                                                        />
                                                    </div>
                                                    <div
                                                        class="w-full h-1/4 flex items-center justify-evenly"
                                                    >
                                                        <el-select
                                                            placeholder="请选择英雄"
                                                            v-model="el_bgChampion"
                                                            @change="onbgChampChange"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            >
                                                            </el-option>
                                                        </el-select>
                                                        <el-select
                                                            placeholder="请选择皮肤"
                                                            v-model="el_bgSkin"
                                                        >
                                                            <el-option
                                                                v-for="item in skinOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            >
                                                            </el-option>
                                                        </el-select>
                                                        <el-button @click="onBgSkinChange">
                                                            <span>修改背景</span>
                                                        </el-button>
                                                    </div>
                                                </div>
                                            </el-dialog>
                                        </div>
                                    </div>
                                </div>
                            </collapse-transition>
                        </div>
                        <div class="card w-full rounded flex flex-col overflow-hidden mt-7">
                            <div
                                class="h-20 px-8 flex items-center cursor-pointer"
                                @click="show2 = !show2"
                            >
                                <span class="font-bold text-xl">自动禁选</span>
                            </div>
                            <hr />
                            <collapse-transition>
                                <div class="px-6" v-if="show2">
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动锁定</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    当启用自动选英时自动确定，如果未启动该选项，软件仅会选择到配置的禁选英雄而不锁定。
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autolock"
                                                v-model:checked="settings.autoBanPick.confirmSelect"
                                            />
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动选择英雄</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在英雄选择`的选择英雄阶段根据配置内容自动选择英雄
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autopick"
                                                v-model:checked="settings.autoBanPick.pick.enable"
                                            />
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">自动禁用英雄</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在英雄选择的禁用阶段根据配置内容自动禁用英雄
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <checkbox
                                                id="autoban"
                                                v-model:checked="settings.autoBanPick.ban.enable"
                                            />
                                        </div>
                                    </div>
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">大乱斗自动交换</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    极地大乱斗模式自动交换英雄(优先级根据英雄选择先后顺序)
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-select
                                                v-model="settings.autoBanPick.roll.swap"
                                                multiple
                                                filterable
                                                collapse-tags
                                                :max-collapse-tags="1"
                                                placeholder="选择大乱斗swap位"
                                                class="w-auto mr-3"
                                            >
                                                <el-option
                                                    v-for="item in championOptions"
                                                    :key="item.value"
                                                    :label="item.label"
                                                    :value="item.value"
                                                />
                                            </el-select>
                                            <checkbox
                                                id="autoroll"
                                                v-model:checked="settings.autoBanPick.roll.enable"
                                            />
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex pb-4">
                                        <div class="w-1/2">
                                            <div class="py-4">
                                                <span class="font-bold text-lg">选取配置</span>
                                            </div>
                                            <div
                                                class="flex flex-col justify-between items-center px-6"
                                            >
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >普通</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="
                                                                settings.autoBanPick.pick.normal
                                                            "
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择普通pick位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >上单</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.pick.top"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择上单pick位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >打野</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.pick.jug"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择打野pick位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >中单</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.pick.mid"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择中单pick位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >射手</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.pick.adc"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择射手pick位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >辅助</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.pick.sup"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择辅助pick位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="w-1/2">
                                            <div class="py-4">
                                                <span class="font-bold text-lg">禁用配置</span>
                                            </div>
                                            <div
                                                class="flex flex-col justify-between items-center px-6"
                                            >
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >普通</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="
                                                                settings.autoBanPick.ban.normal
                                                            "
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择普通ban位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >上单</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.ban.top"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择上单ban位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >打野</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.ban.jug"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择打野ban位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >中单</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.ban.mid"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择中单ban位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >射手</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.ban.adc"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择射手ban位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                                <div class="flex items-center h-10 w-full">
                                                    <div class="w-10">
                                                        <span class="text-sm text-gray-500"
                                                            >辅助</span
                                                        >
                                                    </div>
                                                    <div class="flex-1">
                                                        <el-select
                                                            v-model="settings.autoBanPick.ban.sup"
                                                            multiple
                                                            filterable
                                                            collapse-tags
                                                            :max-collapse-tags="3"
                                                            placeholder="选择辅助ban位"
                                                            class="w-full"
                                                        >
                                                            <el-option
                                                                v-for="item in championOptions"
                                                                :key="item.value"
                                                                :label="item.label"
                                                                :value="item.value"
                                                            />
                                                        </el-select>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </collapse-transition>
                        </div>
                        <div class="card w-full rounded flex flex-col overflow-hidden mt-7">
                            <div
                                class="h-20 px-8 flex items-center cursor-pointer"
                                @click="show3 = !show3"
                            >
                                <span class="font-bold text-xl">其他功能</span>
                            </div>
                            <hr />
                            <collapse-transition>
                                <div class="px-6" v-show="show3">
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">保存本地设置</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    将游戏内的所有设置保存在本地，用于切换账号时覆盖原设置
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="onSaveSetting">
                                                <span class="text-sm text-gray-500">保存设置</span>
                                            </el-button>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">覆盖游戏设置</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    将本地保存的设置覆盖游戏设置（此操作不可逆）
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="onLoadSetting">
                                                <span class="text-sm text-gray-500">覆盖设置</span>
                                            </el-button>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">智能分解战利品</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    智能分解战利品，可以在<span
                                                        class="cursor-pointer underline text-blue-600"
                                                        @click="lootVisible = true"
                                                        >此处</span
                                                    >修改分解规则的配置文件
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="onLootDissovle">
                                                <span class="text-sm text-gray-500">分解碎片</span>
                                            </el-button>
                                        </div>
                                    </div>
                                    <hr />
                                    <div class="flex h-20">
                                        <div class="h-full flex-1 flex flex-col justify-center">
                                            <div>
                                                <span class="text-lg">牛马评分</span>
                                            </div>
                                            <div class="mt-1">
                                                <div class="text-gray-500 text-sm truncate">
                                                    在英雄选择界面发送队友牛马评分
                                                </div>
                                            </div>
                                        </div>
                                        <div class="h-full flex justify-center items-center">
                                            <el-button @click="nmVisible = true">
                                                <span class="text-sm text-gray-500">修改配置</span>
                                            </el-button>
                                        </div>
                                    </div>
                                </div>
                            </collapse-transition>
                        </div>
                    </template>
                    <template v-else>
                        <div class="text-center">
                            <span class="text-lg text-gray-700">未获得设置</span>
                        </div>
                    </template>
                </div>
            </div>
        </div>
        <el-dialog v-model="lootVisible" title="战利品分解配置" width="600px">
            <div class="h-[50vh] overflow-y-auto">
                <div>
                    <div>
                        <span class="text-xl">英雄碎片</span>
                    </div>
                    <div class="py-2 px-5">
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION_RENTAL.enable" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>保留未拥有英雄碎片</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION_RENTAL.sellNotOwned" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>至少保留一个</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION_RENTAL.isRemainOne" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>为英雄代币保留</span>
                            </div>
                            <div>
                                <el-switch
                                    v-model="settings.loot.CHAMPION_RENTAL.isRemainForToken"
                                />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解最低蓝色精粹</span>
                            </div>
                            <div>
                                <el-select
                                    v-model="settings.loot.CHAMPION_RENTAL.sellMinValue"
                                    size="small"
                                >
                                    <el-option
                                        v-for="val in blueEssenceOption"
                                        :key="val"
                                        :label="val"
                                        :value="val"
                                    />
                                </el-select>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div>
                        <span class="text-xl">英雄</span>
                    </div>
                    <div class="py-2 px-5">
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION.enable" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>保留未拥有英雄</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION.sellNotOwned" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>至少保留一个</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION.isRemainOne" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>为英雄代币保留</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.CHAMPION.isRemainForToken" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解最低蓝色精粹</span>
                            </div>
                            <div>
                                <el-select
                                    v-model="settings.loot.CHAMPION.sellMinValue"
                                    size="small"
                                >
                                    <el-option
                                        v-for="val in blueEssenceOption"
                                        :key="val"
                                        :label="val"
                                        :value="val"
                                    />
                                </el-select>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div>
                        <span class="text-xl">皮肤碎片</span>
                    </div>
                    <div class="py-2 px-5">
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.SKIN_RENTAL.enable" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>保留未拥有皮肤碎片</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.SKIN_RENTAL.sellNotOwned" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>至少保留一个</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.SKIN_RENTAL.isRemainOne" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解最低橙色精粹</span>
                            </div>
                            <div>
                                <el-select
                                    v-model="settings.loot.SKIN_RENTAL.sellMinValue"
                                    size="small"
                                >
                                    <el-option
                                        v-for="val in orangeEssenceOption"
                                        :key="val"
                                        :label="val"
                                        :value="val"
                                    />
                                </el-select>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div>
                        <span class="text-xl">皮肤</span>
                    </div>
                    <div class="py-2 px-5">
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.SKIN.enable" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>保留未拥有皮肤</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.SKIN.sellNotOwned" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>至少保留一个</span>
                            </div>
                            <div>
                                <el-switch v-model="settings.loot.SKIN.isRemainOne" />
                            </div>
                        </div>
                        <div class="h-8 leading-8 flex items-ceter justify-between">
                            <div>
                                <span>分解最低橙色精粹</span>
                            </div>
                            <div>
                                <el-select v-model="settings.loot.SKIN.sellMinValue" size="small">
                                    <el-option
                                        v-for="val in orangeEssenceOption"
                                        :key="val"
                                        :label="val"
                                        :value="val"
                                    />
                                </el-select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </el-dialog>
        <el-dialog v-model="nmVisible" title="牛马评分配置" width="600px">
            <div class="py-2 px-5">
                <div class="h-8 leading-8 flex items-ceter justify-between">
                    <div>
                        <span>开启</span>
                    </div>
                    <div>
                        <el-switch v-model="settings.remark.enable" />
                    </div>
                </div>
                <div class="h-8 leading-8 flex items-ceter justify-between">
                    <div>
                        <span>是否排除自己</span>
                    </div>
                    <div>
                        <el-switch v-model="settings.remark.excludeme" />
                    </div>
                </div>
                <div class="h-8 leading-8 flex items-ceter justify-between">
                    <div>
                        <span>发送对象</span>
                    </div>
                    <div>
                        <el-select v-model="settings.remark.type" size="small">
                            <el-option label="所有人" value="ALL" />
                            <el-option label="自己" value="ME" />
                        </el-select>
                    </div>
                </div>
            </div>
        </el-dialog>
    </div>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { checkbox } from '@/components/basic'
import { useGlobalStore } from '@/stores'
import collapseTransition from '@/utils/collapse-transition'
import webConfig from '@/global.config'
import axios from 'axios'
import VlazyImage from 'v-lazy-image'
// pinia
const useGlobal = useGlobalStore()
// ref
const blueEssenceOption = [0, 90, 270, 630, 960, 1260]
const orangeEssenceOption = [0, 500, 900, 1400]
const lootVisible = ref(false)
const nmVisible = ref(false)
const iconVisible = ref(false)
const bgVisible = ref(false)
const el_bgChampion = ref()
const el_bgSkin = ref()
const el_status = ref()
const el_rank = ref()
const el_name = ref()
const el_sign = ref()
const show1 = ref(true)
const show2 = ref(false)
const show3 = ref(false)
const settings = ref(null)
const skinOptions = ref([])
const rank_options = [
    { label: '坚韧黑铁', value: 'IRON' },
    { label: '英勇青铜', value: 'BRONZE' },
    { label: '不屈白银', value: 'SILVER' },
    { label: '荣耀黄金', value: 'GOLD' },
    { label: '华贵铂金', value: 'PLATINUM' },
    { label: '流光翡翠', value: 'EMERALD' },
    { label: '璀璨钻石', value: 'DIAMOND' },
    { label: '超凡大师', value: 'MASTER' },
    { label: '傲视宗师', value: 'GRANDMASTER' },
    { label: '最强王者', value: 'CHALLENGER' },
]
const status_options = [
    { label: '在线', value: 'chat' },
    { label: '离开', value: 'away' },
    { label: '游戏中', value: 'dnd' },
    { label: '离线', value: 'offline' },
    { label: '手机在线', value: 'mobile' },
]
const championOptions = computed(() => {
    let temp = []
    for (let key in webConfig.champions) {
        temp.push({
            value: Number(key),
            label: webConfig.champions[key].label,
        })
    }
    return temp
})
const onbgChampChange = async () => {
    skinOptions.value = []
    if (el_bgChampion.value) {
        let temp = []
        const res = await axios.get(webConfig.baseUrl + '/skin/' + el_bgChampion.value)
        for (let skin of res.data) {
            temp.push({
                value: Number(skin.id),
                label: skin.name,
            })
        }
        skinOptions.value = temp
    }
}

// functions
const onSettingsChange = async () => {
    await axios.post(webConfig.baseUrl + '/change-app-setting', settings.value)
}
const onRankChange = async () => {
    await axios.post(webConfig.baseUrl + '/forgeRank', {
        rtier: el_rank.value,
        rdivision: 'I',
        rqueue: 'RANKED_SOLO_5x5',
    })
}
const onStatusChange = async () => {
    await axios.post(webConfig.baseUrl + `/change-status/${el_status.value}`)
}

const onNameChange = async () => {
    await axios.post(webConfig.baseUrl + '/change-name', `${el_name.value}`)
    el_name.value = ''
}
const onSignChange = async () => {
    await axios.post(webConfig.baseUrl + '/change-sign', `${el_sign.value}`)
    el_sign.value = ''
}
const onCreateLobby = async () => {
    await axios.post(webConfig.baseUrl + '/5v5practice')
}
const onSaveSetting = async () => {
    await axios.post(webConfig.baseUrl + '/save-game-setting')
}
const onLoadSetting = async () => {
    await axios.post(webConfig.baseUrl + '/load-game-setting')
}
const onProfileIconChange = async (id) => {
    const res = await axios.post(webConfig.baseUrl + '/change-profileIcon/' + id)
    if (res) {
        ElMessage('已经更换头像')
    }
}
const onLootDissovle = async () => {
    await axios.post(webConfig.baseUrl + '/loot-dissolve')
}
const onBgSkinChange = async () => {
    if (el_bgSkin.value) {
        const res = await axios.post(webConfig.baseUrl + '/change-bgSkin/' + el_bgSkin.value)
        if (res) {
            ElMessage('已经更换头像')
        }
    }
}
watch(
    settings,
    async (to, prev) => {
        if (prev != null) {
            await onSettingsChange()
            useGlobal.setSetting(settings.value)
        }
    },
    { deep: true },
)
onMounted(async () => {
    await useGlobal.getSetting()
    settings.value = useGlobal.settings
})
</script>
<style lang="scss" scoped>
* {
    user-select: none;
}
.card {
    position: relative;
    background-color: #fff;
    box-shadow: 0 2px 10px -1px #55555514, 0 1px 10px #5555550f, 0 1px 30px #55555508;
}
.elevation {
    box-shadow: 0 7px 30px -4px #55555514, 0 12px 30px 2px #5555550f, 0 5px 30px 4px #55555508 !important;
}
</style>
