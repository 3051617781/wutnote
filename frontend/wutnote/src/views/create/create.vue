<script setup>
    import { ref, onMounted, reactive } from 'vue'
    import { useUserStore } from '@/stores/user'
    import { useRouter } from 'vue-router'
    import { handelImageFile,addNote } from '@/apis/create'
    import { ElMessage } from 'element-plus'
    import { Back } from '@element-plus/icons-vue'

    import MenuBar from "@/views/create/Menubar/menubar.vue"
    import { useEditor, EditorContent } from "@tiptap/vue-3"
    import StarterKit from "@tiptap/starter-kit"
    import Placeholder from "@tiptap/extension-placeholder"
    import Document from "@tiptap/extension-document"
    import Highlight from '@tiptap/extension-highlight'
    import Image from '@tiptap/extension-image'
    import HeadingExtension from '@tiptap/extension-heading'

    // import CodeBlock from '@tiptap/extension-code-block'
    // import CodeBlockLowlight from '@tiptap/extension-code-block-lowlight'
    // import lowlight from 'lowlight'
    // import javascript from 'lowlight/lib/languages/javascript'

    import Table from '@tiptap/extension-table'
    import TableRow from '@tiptap/extension-table-row'
    import TableCell from '@tiptap/extension-table-cell'
    import TableHeader from '@tiptap/extension-table-header'

    const user = useUserStore()
    const router = useRouter()
    const token = ref(localStorage.getItem('token'))

    const CustomTableCell = TableCell.extend({
        addAttributes() {
            return {
                // 展开现有属性,?.是可选链操作符,可以自行百度(懂的大佬当我没说)
                ...this.parent?.(),

                // 添加新的属性
                backgroundColor: {
                    default: null,
                    parseHTML: (element) => element.getAttribute('data-background-color'),
                    renderHTML: (attributes) => ({
                        'data-background-color': attributes.backgroundColor,
                        style: `background-color: ${attributes.backgroundColor}`
                    })
                }
            }
        }
    })
    // lowlight.registerLanguage('javascript', javascript)

// const CodeBlockExtension = CodeBlock.extend({
//   addOptions() {
//     return {
//       highlight: highlight,
//     };
//   },
// });
    const editor = useEditor({
        content: '',
        extensions:[
            Document,
            StarterKit,
            Image,
            // CodeBlock,
            // CodeBlockLowlight.configure({
            //     lowlight,
            // }),
            Highlight.configure({multicolor:true}),
            HeadingExtension.configure({levels:[1,2,3]}),
            Table.configure({
                resizable:true
            }),
            TableRow,
            TableCell,
            TableHeader,
            CustomTableCell,
            Placeholder.configure({
                placeholder:"开始你的笔记创作之旅"
            })
        ]
    }) 

    // 粘贴复制图片
    const handelPaste = async (event) =>{
        // 获取粘贴的数据
        const pasteData = event.clipboardData || window.clipboardData;
        const items = pasteData.items;
        if (items && items.length > 0) {
            for (let item of items) {
                // 检查 item 是不是文件类型
                if (item.kind === 'file') {
                    // 将 item 转换为 File 对象
                    const file = item.getAsFile();
                    if (file && file.type.match('image.*')) {
                        user.isLoading = true;
                        const res = await handelImageFile(file, token.value);
                        if(editor.value){
                            editor.value.commands.insertContent({
                                type: 'image',
                                attrs: {
                                    src: res.url,
                            },
                        });
                        user.isLoading = false;
                            // editor.chain().focus().setImage({ src: res.url }).run()
                        }else{
                            console.log("未被初始化");
                        }
                        
                    }
                }
            }
        }
    }

    // 笔记目录生成
    // const tableOfContents = ref([]);
    // const generateContents = () => {
 
    // };

    // 控制笔记保存信息的提交
    const noteDialogShow = ref(false)
    const noteForm = reactive({
        title:"",
        abstract:"",
        content:"",
        tags:[]
    })
     const rules = {
        "title":[
            { required: true, message: '标题不能为空' }
        ],
        "abstract":[
            { required: true, message: '摘要不能为空' }
    ]}


    const tagIput = ref('')
    const inputVisible = ref(false)
    const showInput = () =>{
        inputVisible.value = true
    }
    // 标签添加
    const handleInputConfirm = () =>{
        noteForm.tags.push(tagIput.value)
        tagIput.value = ''
        inputVisible.value = false
    }
    // 标签删除
    const handleClose = (tag) =>{
        const index = noteForm.tags.indexOf(tag)
        noteForm.tags.splice(index,1)
    }

    // 提交弹窗控制
    const uploadDialogVisible = ref(!user.dialogVisible)
    const returnHome = () =>{
        uploadDialogVisible.value = false;
        router.push('/home');
    }

    // 提交表单
    const noteFormRef = ref(null)
    const noteFormCheck = ()=>{
        noteFormRef.value.validate(async (valid) => {
            if (valid) {  
                // 获取编辑器里面的内容
                noteForm.content = editor.value.getHTML();       
                await addNote(noteForm,token.value); 
                editor.value.commands.clearContent();                     
                noteFormRef.value.resetFields();
            }
      });
    }
    
</script>

<template>
    <div class="create-container">
        <MenuBar :editor="editor"/>
        <div class="editor-contanier">
            <el-scrollbar class="editor-box" style="height: 100%;">
                <div class="scroll-content">
                    <!-- <textarea class="title-input" placeholder="请输入标题"></textarea> -->
                    <editor-content id="editor" :editor="editor"  @paste="handelPaste" style="color:#DCDCDC;"/>
                </div>
            </el-scrollbar> 
            <!-- 图片加载动画 -->
            <div class="loading-box" v-if="user.isLoading">
                <img src="@/assets/loading.jpg" alt="" class="loading">
                <p>图片上传中...</p>
            </div>
            <!-- 提交笔记跳转弹窗 -->
            <el-dialog
                v-model="uploadDialogVisible"
                width="250"
                align-center>
                <span>笔记发布成功!</span>
                <template #footer>
                <div class="dialog-footer">
                    <el-button @click="returnHome">返回首页</el-button>
                    <el-button type="primary" @click="uploadDialogVisible = false">
                    继续编辑
                    </el-button>
                </div>
                </template>
            </el-dialog>
        </div>
        <div class="save-container">
            <div class="save-box">
                <div class="top-box">
                    <p>笔记设置</p>
                    <el-button @click="noteFormCheck">保存笔记</el-button>
                </div>
                <div class="bottom-box">
                    <div class="note-container">
                        <el-form :model="noteForm" ref="noteFormRef" class="note-box" >
                            <el-form-item prop="title" label="标题：" :rules="rules.title">
                                <input v-model="noteForm.title" style="width: 240px"/>
                            </el-form-item>
                            <el-form-item prop="tags" label="标签：">
                            <div class="addtags-box">
                                <input
                                    v-if="inputVisible"
                                    v-model="tagIput"
                                    @keyup.enter="handleInputConfirm"/>
                                <el-button v-else class="button-new-tag" @click="showInput">
                                + 添加标签
                                </el-button>
                                <div class="tags-box">
                                    <el-tag
                                        v-model="noteForm.tags"
                                        v-for="tag in noteForm.tags"
                                        :key="tag"
                                        closable
                                        @close="handleClose(tag)">
                                        {{ tag }}
                                    </el-tag>
                                </div>
                            </div>
                            </el-form-item>
                            <el-form-item prop="abstract" label="摘要：" :rules="rules.abstract">
                                <textarea v-model="noteForm.abstract"
                                        placeholder="请输入对笔记内容的概述" 
                                        cols="10"/>
                            </el-form-item>
                        </el-form>
                    </div>
                </div>
            </div> 
        </div>
    </div> 
</template>

<style lang="scss" scoped>
.create-container{
    background-color: $theme-color;
    display: flex;
    flex-direction: column;
}

.editor-contanier{
    height: 500px;
    display: flex;
    justify-content: center;
    padding: 30px;
    .loading-box{
        position: fixed;
        top: 50%;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        align-items: center;
        img{
            width: 30px;
        }
        p{
            margin-top: 5px;
            color: $text-color;
        }
    } 
}

.editor-box{                                  
    width: 800px;
    padding: 20px 50px;
    background-color: $low-theme-color;
    border-radius: 15px;
    .scroll-content {
        width: 100%;
        overflow-x: hidden;
    }
}


.save-container{
    display: flex;
    justify-content: center;
    margin: 20px 0;
    .save-box{
        width: 850px;
        // padding: 15px;
        background-color: $theme-color;
        border: 2px solid $border-color;
        // background-color: pink;
        color: $theme-text;
        .top-box{
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid $border-color;
            p{
                font-size: 16px;
            }
        }
    }
}
.el-button{
    background-color: $theme-active;
    color: $theme-color;
    border: none;
}
.bottom-box{
    padding: 0 50px;
    .addtags-box{
        .el-tag{
            background-color: $low-theme-color;
            color: $theme-text;
            border: none;
        }
    }
}
.note-container{
    display: flex;
    input{
        height: 28px;
        border-radius: 5px;
    }
}
.note-box{
    .el-form-item{
        margin: 15px 0;
    }
    .addtags-box{
        display: flex;
        flex-direction: column;
        .tags-box{
            margin-top: 10px;
        }
    }
    textarea{
        resize: none;
        width: 500px;
        height: 250px;
        outline: none;
        background-color: #282828;
        border: none;
        color:#DCDCDC;
        font-size: 16px;
        padding: 10px;
    }
}

</style>
<style lang="scss">
.tiptap,.ProseMirror-focused {
    outline: none;
}
.tiptap p.is-editor-empty:first-child::before {
  color: #adb5bd;
  content: attr(data-placeholder);
  float: left;
  height: 0;
  pointer-events: none;
}
.tiptap p{
    margin-top: 10px;
    padding-left: 10px;
    // background-color: pink;
}
.tiptap p:hover{
    // margin-top: 10px;
    padding-left: 6px;
    border-left: 4px solid $theme-active;
}
blockquote{
    margin: 16px 0;
    padding: 20px 0;
    background-color: $block-color;
    border-left: 4px solid $block-border-color !important;
    p{
        margin: 0 !important;
    }
}

// 设置图片上传不在一行显示
.ProseMirror img {
    display: block;
    width: 30%;
}

/* 设置表格宽高 */
.ProseMirror table {
  width: 60%; /* 表格宽度 */
  border-collapse: collapse; /* 边框合并 */
}

.ProseMirror table td,
.ProseMirror table th {
  border: 1px solid #ddd; /* 单元格边框 */
  padding: 2px; /* 单元格内边距 */
  p{
    margin:0;
  }
}

/* 设置表头颜色 */
.ProseMirror table th {
  background-color: #f0f0f0; /* 表头背景颜色 */
}

.el-form-item__label {
  color: $theme-text;
}
blockquote{
  border-left: 3px solid $theme-color; /* 引用块左边的线 */
  color: $text-color; /* 文字颜色 */
  background-color: $theme-color; /* 背景色 */
}

</style>
<style lang="scss">
// .el-dialog{
//     background-color: $low-theme-color;
// } 
.dialog-footer{
    display: flex;
    justify-content: center;
}
</style>