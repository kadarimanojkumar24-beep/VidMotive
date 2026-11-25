
package com.vidmotive

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.LocalContext

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val incoming = if (intent?.action == Intent.ACTION_SEND)
            intent.getStringExtra(Intent.EXTRA_TEXT) ?: "" else ""

        setContent {
            VidMotiveScreen(initialUrl = incoming)
        }
    }
}

@Composable
fun VidMotiveScreen(initialUrl: String) {
    var url by remember { mutableStateOf(initialUrl) }
    var platform by remember { mutableStateOf("") }
    var message by remember { mutableStateOf("Share or paste a video link to begin.") }
    var score by remember { mutableStateOf("—") }
    val context = LocalContext.current

    fun analyze() {
        val u=url.lowercase()
        platform = when {
            "instagram.com" in u -> "Instagram Reel / Post"
            "youtube.com" in u || "youtu.be" in u -> "YouTube"
            "tiktok.com" in u -> "TikTok"
            "facebook.com" in u || "fb.watch" in u -> "Facebook"
            "x.com" in u || "twitter.com" in u -> "X"
            else -> "Video / Web link"
        }
        score = when(platform) {
            "Instagram Reel / Post" -> "91%"
            "YouTube" -> "86%"
            "TikTok" -> "89%"
            "Facebook" -> "82%"
            "X" -> "78%"
            else -> "75%"
        }
        message = "Video link detected. Open the original content to watch it. " +
                  "This screen provides a quick motivation layer before you watch."
    }

    MaterialTheme(colorScheme = darkColorScheme(
        primary = Color(0xFF5867F2),
        background = Color(0xFF080D1C),
        surface = Color(0xFF11182C)
    )) {
        Surface(Modifier.fillMaxSize()) {
            Column(
                Modifier.fillMaxSize().padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(14.dp)
            ) {
                Text("✦ VIDMOTIVE AI", fontSize=22.sp, fontWeight=FontWeight.Bold)
                Text("Copy/share a video link and let the widget detect it.",
                    color=Color(0xFF9AA8CA))

                OutlinedTextField(
                    value=url, onValueChange={url=it},
                    modifier=Modifier.fillMaxWidth(),
                    label={Text("Video URL")},
                    singleLine=true
                )

                Row(horizontalArrangement=Arrangement.spacedBy(10.dp)) {
                    Button(onClick={analyze}, modifier=Modifier.weight(1f)) {
                        Text("ANALYZE")
                    }
                    OutlinedButton(onClick={
                        if(url.isNotBlank()) {
                            val i=Intent(Intent.ACTION_VIEW, Uri.parse(url))
                            // Browser/social app handles the original URL.
                            context.startActivity(i)
                        }
                    }, modifier=Modifier.weight(1f)) {
                        Text("OPEN")
                    }
                }

                Card(
                    colors=CardDefaults.cardColors(containerColor=Color(0xFF11182C)),
                    shape=RoundedCornerShape(22.dp),
                    modifier=Modifier.fillMaxWidth()
                ) {
                    Column(Modifier.padding(18.dp), verticalArrangement=Arrangement.spacedBy(10.dp)) {
                        Text(if(platform.isBlank()) "Waiting for link…" else "● $platform",
                            fontWeight=FontWeight.Bold)
                        Text(message, color=Color(0xFFDCE5FF))
                        Text("Motivation potential  $score",
                            color=Color(0xFF8EE6FF), fontSize=21.sp,
                            fontWeight=FontWeight.Bold)
                    }
                }

                Spacer(Modifier.weight(1f))
                Text("Android: use Share → VidMotive from Instagram/YouTube/etc.",
                    color=Color(0xFF7F8BAA), fontSize=13.sp)
            }
        }
    }
}
