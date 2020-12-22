var idx = 1;
function change_song() 
{
    var arr = new Array("background_audio1.mp3", "background_audio2.mp3",
        "background_audio3.mp3", "background_audio4.mp3", "background_audio5.mp3", "background_audio6.mp3");
    var bg_audio = document.getElementById('background_audio');
    bg_audio.pause();
    var music_file = "../static/audio/" + arr[idx];
    bg_audio.src = music_file;
    bg_audio.play();
    idx = (idx + 1) % 6;
}
var idx_bg = 1;
function change_bg_picture()
{
    var arr = new Array("background_video.mp4", "background_video2.mp4", "background_video3.mp4");
    var bg_file = "../static/video/" + arr[idx_bg];
    var bg_video = document.getElementById('background_video');
    bg_video.src = bg_file;
    idx_bg = (idx_bg + 1) % 3;
}

function cancel()
{
    var btn = document.getElementById('cancel');
    if (btn.value == "点击收藏")
    {
        btn.setAttribute("value", "已收藏");
        btn.setAttribute("class", "mybutton2_collected");
    }
    else
    {
        btn.setAttribute("value", "点击收藏");
        btn.setAttribute("class", "mybutton2");
    }
}
function collect()
{
    var btn = document.getElementById('store');
    if (btn.value == "点击收藏")
    {
        btn.setAttribute("value", "已收藏");
        btn.setAttribute("class", "mybutton2_collected");
    }
    else
    {
        btn.setAttribute("value", "点击收藏");
        btn.setAttribute("class", "mybutton2");
    }
}
function hide()
{
    var t1 = document.getElementById("hid_btn");
    var t2 = document.getElementById("console_box");
    if (t1.value == "<")
    {
        t1.setAttribute("value", ">");
        t2.style.height = "30px";
        t2.style.border = "0px solid rgba(0,0,0,0)";
        t2.style.width = "30px";
        t1.style.left = "15%";
    }
    else
    {
        t1.setAttribute("value", "<");
        t2.style.height = "220px";
        t2.style.border = "5px solid rgba(0,0,0,0.8)";
        t2.style.width = "20%";
        t1.style.left = "90%";
    }
}
function hide_ad()
{
    var t1 = document.getElementById("hid_btn2");
    var t2 = document.getElementById("advertisement");
    if (t1.value == "<")
    {
        t1.setAttribute("value", ">");
        t2.style.height = "30px";
        t2.style.width = "30px";
        t1.style.left = "15%";
    }
    else
    {
        t1.setAttribute("value", "<");
        t2.style.height = "40%";
        t2.style.width = "20%";
        t1.style.left = "90%";
    }
}


$document.read
    (
        function ()
        {
            $(".pic").imgbox
                (
                    {
                        'speedIn': 0,
                        'speedOut': 0,
                        'alignment': center,
                        'overlayShow': true,
                        'allowMultiple': false
                    }
                );
        }
    );

function night()
{
    var x = document.getElementById("day_night_change");
    var y = document.getElementById("mid_content_box");
    var z = document.getElementById("film_information");
    var t = document.getElementById("title_of_film");
    if (x.value == "night")
    {
        x.setAttribute("value", "day");
        y.style.background = " rgba(0,0,0,0.8)";
        y.style.color = "white";
        z.style.color = "white";
        t.style.color = "yellow";
    }
    else
    {
        x.setAttribute("value", "night");
        y.style.background = " rgba(255,255,255,0.7)";
        y.style.color = "black";
        z.style.color = "black";
        t.style.color = "purple";
    }
}