function judgeUsername()
{

    var checkUsername = document.getElementById('Uname').value;
    var war = document.getElementById('warUsername');
    if (checkUsername == '' || checkUsername == null)
    {
        war.innerHTML = "请输入不为空的用户名！";
        return false;
    }
    else
    {
        var reg1 = /[\s]/;
        if (reg1.test(checkUsername))
        {
            war.innerHTML = '该用户名与格式要求不符，请重新输入！';
            return false;
        }
        else
        {
            document.getElementById('regiForm').submit();
            return true;
        }
    }
}

function judgeUsername1()
{
    var checkUsername = document.getElementById('warUsername').value;
    if (checkUsername == "请输入不为空的用户名！" || checkname == "该用户名已经被占用，请重新输入!")
    {
        return false;
    }
    else if (checkUsername == "该用户名可用")
    {
        return true;
    }
}


function judgeRegiPassword_available()
{
    var checkPassword = document.getElementById('Pawd').value;
    var war = document.getElementById('warPassword');
    var reg1 = /[\s]/;
    var pwdRegex = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9])');
    var reg2 = /[\S]{8,20}$/;
    if (!reg1.test(checkPassword))
    {
        document.getElementById('r1').style.color = "lightblue";
    }
    else
    {
        document.getElementById('r1').style.color = "red";
    }
    if (reg2.test(checkPassword))
    {
        document.getElementById('r2').style.color = 'lightblue';
    }
    else
    {
        document.getElementById('r2').style.color = "red";
    }
    if (pwdRegex.test(checkPassword))
    {
        document.getElementById('r3').style.color = 'lightblue';
    }
    else
    {
        document.getElementById('r3').style.color = "red";
    }
}
