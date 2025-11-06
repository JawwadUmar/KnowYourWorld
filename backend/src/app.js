require("dotenv").config();
const express = require("express");
const app = express();
const axios = require("axios");
const { GoogleGenerativeAI } = require("@google/generative-ai");

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

app.get("/", async (req, res) => {
    let { data } = await axios.get("http://127.0.0.1:8000/extract");
    data = data + "generate 5 tough questions for the students who are preparing for upsc examinations. Consider the above data as study material. at the end of 5 questions provide the soluition. also I'm sending the data from your response as res.send directly, so format it accordingly to show in my website";
    res.send(await generateContent(data));
});

async function generateContent(prompt) {
    const result = await model.generateContent(prompt);
    return result.response.text();
}

module.exports = app;
