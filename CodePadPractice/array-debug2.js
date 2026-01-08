// Problem 1: Find Longest Word
//Buggy Code:
function findLongest(sentence) {
  let words = sentence.split(' ');
  let longest = words[0];
  
  for(let i = 0; i < words.length; i++){
    if(words[i].length >= longest.length){
      longest = words[i];
    }
  }
  
  return longest;
}

//Actual:
function findLongest(sentence) {
  if (sentence.trim().length === 0){
    return ""
  }
  let words = sentence.split(' ');
  let longest = words[0];
  
  for(let i = 0; i < words.length; i++){
    if(words[i].length > longest.length){
      longest = words[i];
    }
  }
  
  return longest;
}


// console.log(findLongest("The quick brown fox jumps"));
// // Expected: "quick"
// // Actual: "jumps"

// console.log(findLongest(""));
// // Expected: ""
// // Actual: crashes with error

// console.log(findLongest("a bb ccc bb"));
// // Expected: "ccc"
// // Actual: "ccc" ✓


// Problem 2: Count Vowels
// Buggy:
function countVowels(str) {
  let vowels = ['a', 'e', 'i', 'o', 'u'];
  let count = 0;
  
  for(let i = 0; i < str.length; i++){
    if(vowels.includes(str[i])){
      count++;
    }
  }
  
  return count;
}

// Actual:
function countVowels(str) {
  let vowels = ['a', 'e', 'i', 'o', 'u'];
  let count = 0;
  
  for(let i = 0; i < str.length; i++){
    if(vowels.includes(str[i].toLowerCase())){
      count++;
    }
  }
  
  return count;
}

console.log(countVowels("Hello World"));
// Expected: 3
// Actual: 2

console.log(countVowels("AEIOU"));
// Expected: 5
// Actual: 0

console.log(countVowels("xyz"));
// Expected: 0
// Actual: 0 ✓

console.log(countVowels(""));
// Expected: 0
// Actual: 0 ✓


// Problem 3: Deep Clone Object
// Buggy:
function deepClone(obj) {
  let clone = {};
  
  for(let key in obj){
    clone[key] = obj[key];
  }
  
  return clone;
}


// Actual:
function deepClone(obj) {
  let clone = {};
  
  for(let key in obj){
    clone[key] = structuredClone(obj[key]); // To make a deep copy
  }
  return clone;
}

//Classic way of doing it is to Recursively clone each property

let obj1 = {a: 1, b: {c: 2}};
let clone1 = deepClone(obj1);
clone1.b.c = 999;
console.log(obj1.b.c);
// Expected: 2 (original unchanged)
// Actual: 999 (original was modified!)

let obj2 = {x: [1, 2, 3]};
let clone2 = deepClone(obj2);
clone2.x.push(4);
console.log(obj2.x);
// Expected: [1, 2, 3] (original unchanged)
// Actual: [1, 2, 3, 4] (original was modified!)

// Problem 4: Find Missing Number
// Buggy:
function findMissing(arr) {
  let n = arr.length;
  let expectedSum = (n * (n + 1)) / 2;
  let actualSum = 0;
  
  for(let i = 0; i < arr.length; i++){
    actualSum += arr[i];
  }
  
  return expectedSum - actualSum;
}

// Actual:
function findMissing(arr) {
  let n = arr.length + 1;
  let expectedSum = (n * (n + 1)) / 2;
  let actualSum = 0;
  
  for(let i = 0; i < arr.length; i++){
    actualSum += arr[i];
  }
  
  return expectedSum - actualSum;
}


console.log(findMissing([1, 2, 4, 5, 6]));
// Expected: 3
// Actual: 0

console.log(findMissing([2, 3, 4, 5, 6, 7, 8, 9, 10]));
// Expected: 1
// Actual: 0

console.log(findMissing([1, 2, 3, 5]));
// Expected: 4
// Actual: 0
