package com.example.sudoku_app

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.util.*
import kotlin.concurrent.schedule

class PuzzleMode : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_puzzle_mode)

        val easy = findViewById<Button>(R.id.easy)
        val med = findViewById<Button>(R.id.medBtn)
        val hard = findViewById<Button>(R.id.hardBtn)
        easy.setOnClickListener{
            val values=Request(2,null,0)
            API.getApi()?.sendAllValues(values)?.enqueue(object: Callback<Any> {

                override fun onResponse(call: Call<Any>, response: Response<Any>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@PuzzleMode,
                            "Generate Easy", Toast.LENGTH_LONG).show()

                        Timer("SettingUp", false).schedule(800) {
                            this@PuzzleMode.finish()
                        }


                    }
                }

                override fun onFailure(call: Call<Any>, t: Throwable) {
                    Toast.makeText(this@PuzzleMode,
                        "Generate Easy Failed", Toast.LENGTH_SHORT).show()
                    println(t.message)
                }

            })

        }

        med.setOnClickListener{
            val values=Request(2,null,1)
            API.getApi()?.sendAllValues(values)?.enqueue(object: Callback<Any> {

                override fun onResponse(call: Call<Any>, response: Response<Any>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@PuzzleMode,
                            "Generate Medium", Toast.LENGTH_LONG).show()

                        Timer("SettingUp", false).schedule(800) {
                            this@PuzzleMode.finish()
                        }
                    }
                }

                override fun onFailure(call: Call<Any>, t: Throwable) {
                    Toast.makeText(this@PuzzleMode,
                        "Generate Medium Failed", Toast.LENGTH_SHORT).show()
                    println(t.message)
                }

            })
        }

        hard.setOnClickListener{
            val values=Request(2,null,2)
            API.getApi()?.sendAllValues(values)?.enqueue(object: Callback<Any> {

                override fun onResponse(call: Call<Any>, response: Response<Any>) {
                    if (response.isSuccessful) {
                        Toast.makeText(this@PuzzleMode,
                            "Generate Hard", Toast.LENGTH_LONG).show()

                        Timer("SettingUp", false).schedule(800) {
                            this@PuzzleMode.finish()
                        }
                    }
                }

                override fun onFailure(call: Call<Any>, t: Throwable) {
                    Toast.makeText(this@PuzzleMode,
                        "Generate Hard Failed", Toast.LENGTH_SHORT).show()
                    println(t.message)
                }

            })
        }
    }
}