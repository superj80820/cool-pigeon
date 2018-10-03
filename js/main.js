function getCookie(e) {
    for (var o = e + "=", t = document.cookie.split(";"), s = 0; s < t.length; s++) {
        var i = t[s].trim();
        if (0 == i.indexOf(o)) return i.substring(o.length, i.length)
    }
    return ""
}

function setCookie(e, o, t) {
    var s = new Date;
    s.setTime(s.getTime() + 24 * t * 60 * 60 * 1e3);
    var i = "expires=" + s.toGMTString();
    document.cookie = e + "=" + o + "; " + i
}

function showSplash() {
    currentstate = states.SplashScreen, velocity = 0, position = 180, rotation = 0, score = 0, $("#player").css({
        y: 0,
        x: 0
    }), updatePlayer($("#player")), soundSwoosh.stop(), soundSwoosh.play(), $(".pipe").remove(), pipes = new Array, $(".animated").css("animation-play-state", "running"), $(".animated").css("-webkit-animation-play-state", "running"), $("#splash").transition({
        opacity: 1
    }, 2e3, "ease")
}

function startGame() {
    currentstate = states.GameScreen, $("#splash").stop(), $("#splash").transition({
        opacity: 0
    }, 500, "ease"), setBigScore(), debugmode && $(".boundingbox").show();
    var e = 1e3 / 60;
    loopGameloop = setInterval(gameloop, e), loopPipeloop = setInterval(updatePipes, 1400), playerJump()
}

function updatePlayer(e) {
    rotation = Math.min(velocity / 10 * 90, 90), $(e).css({
        rotate: rotation,
        top: position
    })
}

function gameloop() {
    var e = $("#player");
    velocity += gravity, position += velocity, updatePlayer(e);
    var o = document.getElementById("player").getBoundingClientRect(),
        t = 34,
        s = 24,
        i = t - 8 * Math.sin(Math.abs(rotation) / 90),
        a = (s + o.height) / 2,
        n = (o.width - i) / 2 + o.left,
        r = (o.height - a) / 2 + o.top,
        c = n + i,
        p = r + a;
    if (debugmode) {
        var l = $("#playerbox");
        l.css("left", n), l.css("top", r), l.css("height", a), l.css("width", i)
    }
    if (o.bottom >= $("#land").offset().top) return void playerDead();
    var u = $("#ceiling");
    if (r <= u.offset().top + u.height() && (position = 0), null != pipes[0]) {
        var d = pipes[0],
            h = d.children(".pipe_upper"),
            g = h.offset().top + h.height(),
            m = h.offset().left - 2,
            y = m + pipewidth,
            f = g + pipeheight;
        if (debugmode) {
            var l = $("#pipebox");
            l.css("left", m), l.css("top", g), l.css("height", pipeheight), l.css("width", pipewidth)
        }
        return c > m && !(r > g && f > p) ? void playerDead() : void(n > y && (pipes.splice(0, 1), playerScore()))
    }
}

function screenClick() {
    currentstate == states.GameScreen ? playerJump() : currentstate == states.SplashScreen && startGame()
}

function playerJump() {
    velocity = jump, soundJump.stop(), soundJump.play()
}

function setBigScore(e) {
    var o = $("#bigscore");
    if (o.empty(), !e)
        for (var t = score.toString().split(""), s = 0; s < t.length; s++) o.append("<img src='assets/font_big_" + t[s] + ".png' alt='" + t[s] + "'>")
}

function setSmallScore() {
    var e = $("#currentscore");
    e.empty();
    for (var o = score.toString().split(""), t = 0; t < o.length; t++) e.append("<img src='assets/font_small_" + o[t] + ".png' alt='" + o[t] + "'>")
}

function setHighScore() {
    var e = $("#highscore");
    e.empty();
    for (var o = highscore.toString().split(""), t = 0; t < o.length; t++) e.append("<img src='assets/font_small_" + o[t] + ".png' alt='" + o[t] + "'>")
}

function setMedal() {
    var e = $("#medal");
    return e.empty(), 10 > score ? !1 : (score >= 10 && (medal = "bronze"), score >= 20 && (medal = "silver"), score >= 30 && (medal = "gold"), score >= 40 && (medal = "platinum"), e.append('<img src="assets/medal_' + medal + '.png" alt="' + medal + '">'), !0)
}

function playerDead() {
    $(".animated").css("animation-play-state", "paused"), $(".animated").css("-webkit-animation-play-state", "paused");
    var e = $("#player").position().top + $("#player").width(),
        o = flyArea,
        t = Math.max(0, o - e);
    $("#player").transition({
        y: t + "px",
        rotate: 90
    }, 1e3, "easeInOutCubic"), currentstate = states.ScoreScreen, clearInterval(loopGameloop), clearInterval(loopPipeloop), loopGameloop = null, loopPipeloop = null, isIncompatible.any() ? showScore() : soundHit.play().bindOnce("ended", function() {
        soundDie.play().bindOnce("ended", function() {
            showScore()
        })
    })
    
    $.ajax({
        type: 'GET',
        url: 'https://905768bd.ngrok.io',
        dataType: 'json',
          success: function(test_dic) {
            // $('table').remove();
            //   var item1 ="<tbody>"
            //   var i;
            //   test_j = test_dic
            //   n = test_j.length
  
            //   var item = '<table><thead><tr><th>觀眾姓名</th><th>附加圖片</th><th>問題</th><th>留言時間</th></tr></thead>';
            //   for (i=n-1;i>=0;i--){
            //     $.cookie("ButtonImage_"+i,test_j[i].image);
            //     var name = test_j[i].name;
            //     var time = test_j[i].timestamp;
            //     var id = test_j[i].name;
            //     if (test_j[i].image=='null' || test_j[i].image==null){
            //       image='<input type=button onclick="show_image(this)" id="ButtonImage_'+i+'" value="無">'  
            //     }else{
            //       image='<input type=button onclick="show_image(this)" id="ButtonImage_'+i+'" value="顯示">'
            //     }
                
            //     item1 += '<tr><td>'+name+'</td><td>'+image+'</td><td>'+test_j[i].say+'</td><td>'+time+'</td></tr>';
            //   }
            //   var item2 = '</tbody></table>';
            //   $ulT.append(item+item1+item2);
              
          }
    });

}

function showScore() {
    $("#scoreboard").css("display", "block"), setBigScore(!0), score > highscore && (highscore = score, setCookie("highscore", highscore, 999)), setSmallScore(), setHighScore();
    var e = setMedal();
    soundSwoosh.stop(), soundSwoosh.play(), $("#scoreboard").css({
        y: "40px",
        opacity: 0
    }), $("#replay").css({
        y: "40px",
        opacity: 0
    }), $("#scoreboard").transition({
        y: "0px",
        opacity: 1
    }, 600, "ease", function() {
        soundSwoosh.stop(), soundSwoosh.play(), $("#replay").transition({
            y: "0px",
            opacity: 1
        }, 600, "ease"), e && ($("#medal").css({
            scale: 2,
            opacity: 0
        }), $("#medal").transition({
            opacity: 1,
            scale: 1
        }, 1200, "ease"))
    }), replayclickable = !0
}

function playerScore() {
    score += 1, soundScore.stop(), soundScore.play(), setBigScore()
}

function updatePipes() {
    $(".pipe").filter(function() {
        return $(this).position().left <= -100
    }).remove();
    var e = 80,
        o = flyArea - pipeheight - 2 * e,
        t = Math.floor(Math.random() * o + e),
        s = flyArea - pipeheight - t,
        i = $('<div class="pipe animated"><div class="pipe_upper" style="height: ' + t + 'px;"></div><div class="pipe_lower" style="height: ' + s + 'px;"></div></div>');
    $("#flyarea").append(i), pipes.push(i)
}
var debugmode = !1,
    states = Object.freeze({
        SplashScreen: 0,
        GameScreen: 1,
        ScoreScreen: 2
    }),
    currentstate, gravity = .25,
    velocity = 0,
    position = 180,
    rotation = 0,
    jump = -4.6,
    flyArea = $("#flyarea").height(),
    score = 0,
    highscore = 0,
    pipeheight = 90,
    pipewidth = 52,
    pipes = new Array,
    replayclickable = !1,
    volume = 30,
    soundJump = new buzz.sound("assets/sounds/sfx_wing.ogg"),
    soundScore = new buzz.sound("assets/sounds/sfx_point.ogg"),
    soundHit = new buzz.sound("assets/sounds/sfx_hit.ogg"),
    soundDie = new buzz.sound("assets/sounds/sfx_die.ogg"),
    soundSwoosh = new buzz.sound("assets/sounds/sfx_swooshing.ogg");
buzz.all().setVolume(volume);
var loopGameloop, loopPipeloop;
$(document).ready(function() {
    "?debug" == window.location.search && (debugmode = !0), "?easy" == window.location.search && (pipeheight = 200);
    var e = getCookie("highscore");
    "" != e && (highscore = parseInt(e)), showSplash()
}), $(document).keydown(function(e) {
    32 == e.keyCode && (currentstate == states.ScoreScreen ? $("#replay").click() : screenClick())
}), "ontouchstart" in window ? $(document).on("touchstart", screenClick) : $(document).on("mousedown", screenClick), $("#replay").click(function() {
    replayclickable && (replayclickable = !1, soundSwoosh.stop(), soundSwoosh.play(), $("#scoreboard").transition({
        y: "-40px",
        opacity: 0
    }, 1e3, "ease", function() {
        $("#scoreboard").css("display", "none"), showSplash()
    }))
});
var isIncompatible = {
    Android: function() {
        return navigator.userAgent.match(/Android/i)
    },
    BlackBerry: function() {
        return navigator.userAgent.match(/BlackBerry/i)
    },
    iOS: function() {
        return navigator.userAgent.match(/iPhone|iPad|iPod/i)
    },
    Opera: function() {
        return navigator.userAgent.match(/Opera Mini/i)
    },
    Safari: function() {
        return navigator.userAgent.match(/OS X.*Safari/) && !navigator.userAgent.match(/Chrome/)
    },
    Windows: function() {
        return navigator.userAgent.match(/IEMobile/i)
    },
    any: function() {
        return isIncompatible.Android() || isIncompatible.BlackBerry() || isIncompatible.iOS() || isIncompatible.Opera() || isIncompatible.Safari() || isIncompatible.Windows()
    }
};
"serviceWorker" in navigator && navigator.serviceWorker.register("../service-worker.js").then(function(e) {
    console.log("ServiceWorker registration successful with scope: ", e.scope)
})["catch"](function(e) {
    console.log("ServiceWorker registration failed: ", e)
});