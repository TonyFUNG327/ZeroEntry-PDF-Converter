import { createWorker } from "tesseract.js";

const imagePath = new URL("./rendered/page-1.png", import.meta.url).pathname;
const worker = await createWorker("eng");
const result = await worker.recognize(imagePath);
await worker.terminate();
console.log(result.data.text.slice(0, 2000));
