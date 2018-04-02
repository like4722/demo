function addLoadEvent(func){
    var oldonload = window.onload;
    if(typeof window.onload !='function'){
        window.onload = func;
    }
    else{
        window.onload = function(){
            oldonload();
            func();
        }
    }
}

function addClass(element,value) {
    if(!element.className){
        element.className =value;
    }
    else{
        newClassName = element.className;
        newClassName += " ";
        newClassName += value;
        element.className = newClassName;
    }

}
/*奇偶数行颜色设置 目前有BUG*/
function stripeTables(){
    if(!document.getElementsByTagName)
        return false;
    var tables = document.getElementsByTagName("table");
    var odd,rows;
    for(var i=0;i<tables.length;i++){
        odd = false;
        rows = tables[i].getElementsByTagName("tr");
        for(var j=0;j<rows.length;j++){
            if(odd==true){
                rows[j].style.backgroundColor = "#ffc";
                odd = false;
            }
            else{
                odd = true;
            }
        }

    }
}
/*链接高亮*/
function highlightRows() {
    if(!document.getElementsByTagName)
        return false;
    var rows = document.getElementsByTagName("tr");
    for (var i=0;i<rows.length;i++){
        rows[i].oldClassName = rows[i].className;
        rows[i].onmouseover = function(){
            addClass(this,"highlight");
        }
        rows[i].onmouseover = function(){
            this.className = this.oldClassName;
        }
    }
}
/*表单字段焦点*/
function focusLables() {
    if(!document.getElementsByTagName)
        return false;
    var labels = document.getElementsByTagName("label");
    for(var i=0;i<labels.length;i++){
        if(!labels[i].getAttribute("for"))
            continue;
        labels[i].onclick = function(){
            var id = this.getAttribute("for");
            if(!document.getElementById(id))
                return false;
            var element = document.getElementById(id);
            element.focus();
        }
    }
}
function goPage(pno){
    var itable = document.getElementById("showall");
    var num = itable.rows.length;//表格所有行数(所有记录数)
    console.log(num);
    var totalPage = 0;//总页数
    var pageSize = 16;//每页显示行数
    //总共分几页
    if(num/pageSize > parseInt(num/pageSize)){
        totalPage=parseInt(num/pageSize)+1;
    }else{
        totalPage=parseInt(num/pageSize);
    }
    var currentPage = pno;//当前页数
    var startRow = (currentPage - 1) * pageSize+1;//开始显示的行  31
    var endRow = currentPage * pageSize;//结束显示的行   40
    endRow = (endRow > num)? num : endRow;    //40
    console.log(endRow);
    //遍历显示数据实现分页
    for(var i=1;i<(num+1);i++){
        var irow = itable.rows[i-1];
        if(i>=startRow && i<=endRow){
            irow.style.display = "table-row";
        }else{
            irow.style.display = "none";
        }
    }
    var pageEnd = document.getElementById("pageEnd");
    var tempStr = "<span>共"+totalPage+"页</span>";


//.bind("click",{"newPage":pageIndex},function(event){
//        goPage((pageIndex-1)*pageSize+1,(pageIndex-1)*pageSize+pageSize);
//    }).appendTo('#pages');
    if(currentPage>1){
        tempStr += "<span class='btn' href=\"#\" onClick=\"goPage("+(1)+")\">首页</span>";
        tempStr += "<span class='btn' href=\"#\" onClick=\"goPage("+(currentPage-1)+")\">上一页</span>"
    }else{
        tempStr += "<span class='btn'>首页</span>";
        tempStr += "<span class='btn'>上一页</span>";
    }

    for(var pageIndex= 1;pageIndex<totalPage+1;pageIndex++){
        tempStr += "<a onclick=\"goPage("+pageIndex+")\"><span>"+ pageIndex +" "+"</span></a>";
    }

    if(currentPage<totalPage){
        tempStr += "<span class='btn' href=\"#\" onClick=\"goPage("+(currentPage+1)+")\">下一页</span>";
        tempStr += "<span class='btn' href=\"#\" onClick=\"goPage("+(totalPage)+")\">尾页</span>";
    }else{
        tempStr += "<span class='btn'>下一页</span>";
        tempStr += "<span class='btn'>尾页</span>";
    }

    document.getElementById("barcon").innerHTML = tempStr;

}
/*表格分页*/

function forward(){
    if(document.getElementById("id_username").value){

        alert("上传成功！");
        return true;

    }
    else{
        alert("用户名为空或文件未上传，请重新再试！");
        return false;

    }
}
//获取select选中的text值
function getSelectedtext(){
    var obj=document.getElementsByTagName('select');
    for(i=0;i<obj.length;i++){
        if(obj[i].selected==true){
            console.log(obj[i].innerText);
            return obj[i].innerText;
        }

    }


}


addLoadEvent(stripeTables);
addLoadEvent(highlightRows);
addLoadEvent(focusLables);
