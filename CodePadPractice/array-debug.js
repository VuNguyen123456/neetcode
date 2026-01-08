// --------- 1 Problem 1: Remove Duplicates from Array
//Buggy Code:
function removeDuplicates(arr) {
  let result = [];
  for(let i = 0; i <= arr.length; i++){
    if(!result.includes(arr[i])){
      result.push(arr[i]);
    }
  }
  return result;
}

//Actual:
function removeDuplicates(arr) {
  let result = [];
  for(let i = 0; i < arr.length; i++){
    if(!result.includes(arr[i])){
      result.push(arr[i]);
    }
  }
  return result;
}


// console.log(removeDuplicates([1, 2, 2, 3, 4, 4, 5])); 
// // Expected: [1, 2, 3, 4, 5]
// // Actual: [1, 2, 3, 4, 5, undefined]

// console.log(removeDuplicates([])); 
// // Expected: []
// // Actual: [undefined]

// console.log(removeDuplicates([1, 1, 1])); 
// // Expected: [1]
// // Actual: [1, undefined, undefined]

// --------- 2 Problem 2: Group Items by Category
// Buggy:
function groupBy(arr, property) {
  let result = {};
  for(let i = 0; i < arr.length; i++){
    let key = arr[i][property];
    if(!result[key]){
      result[key] = 0;
    }
    result[key]++;
  }
  return result;
}

//Actual:
function groupBy(arr, property) {
  let result = {};
  for(let i = 0; i < arr.length; i++){
    let key = arr[i][property];
    if(!result[key]){
      result[key] = [];
    }
    result[key].push(arr[i]);
  }
  return result;
}


// let items = [
//   {name: 'apple', type: 'fruit'},
//   {name: 'carrot', type: 'vegetable'},
//   {name: 'banana', type: 'fruit'}
// ];

// console.log(groupBy(items, 'type'));
// // Expected: {
// //   fruit: [{name: 'apple', type: 'fruit'}, {name: 'banana', type: 'fruit'}],
// //   vegetable: [{name: 'carrot', type: 'vegetable'}]
// // }
// // Actual: { fruit: 2, vegetable: 1 }

// console.log(groupBy([], 'type'));
// // Expected: {}
// // Actual: {}  ✓ (This one works)

// --------- 3 Problem 3: Find First Non-Repeating Character
// Buggy:
function firstUnique(str) {
  let counts = {};
  
  for(let i = 0; i < str.length; i++){
    let char = str[i];
    if(!counts[char]){
      counts[char] = 0;
    }
    counts[char]++;
  }
  
  for(let char in counts){
    if(counts[char] = 1){ // chould be === not =
      return char;
    }
  }
}

//Acutal
function firstUnique(str) {
  let counts = {};
  
  for(let i = 0; i < str.length; i++){
    let char = str[i];
    if(!counts[char]){
      counts[char] = 0;
    }
    counts[char]++;
  }

  for(let i = 0; i < str.length; i++){
    let char = str[i];
    if(counts[char] === 1){
        return char;
    }
  }
  return null

}


// console.log(firstUnique("leetcode"));
// // Expected: "l"
// // Actual: "t"

// console.log(firstUnique("aabbcc"));
// // Expected: null
// // Actual: undefined

// console.log(firstUnique("aAbBcC"));
// // Expected: "a"
// // Actual: "A"

// --------- Problem 4: Merge Sorted Arrays
// Buggy:
function mergeSorted(arr1, arr2) {
  let result = [];
  let i = 0, j = 0;
  
  while(i <= arr1.length && j <= arr2.length){
    if(arr1[i] < arr2[j]){
      result.push(arr1[i]);
      i++;
    } else {
      result.push(arr2[j]);
      j++;
    }
  }
  
  return result;
}

//Acutal
function mergeSorted(arr1, arr2) {
  let result = [];
  let i = 0, j = 0;
  
  while(i < arr1.length && j < arr2.length){ // These stop when 1 of the array is done but don't know which one
    if(arr1[i] < arr2[j]){
      result.push(arr1[i]);
      i++;
    } else {
      result.push(arr2[j]);
      j++;
    }
  }
  // Because the above array stop when 1 of the array is done but don't know which one
  // You will need to add remaining of 1 or the other array back
  while(i < arr1.length){
    result.push(arr1[i]);
    i++;
  }
  // OR
  while(j < arr2.length){
    result.push(arr2[j]);
    j++;
  }
  return result;
}

// console.log(mergeSorted([1, 3, 5], [2, 4, 6]));
// // Expected: [1, 2, 3, 4, 5, 6]
// // Actual: [1, 2, 3, 4, 5, 6, undefined, undefined, undefined]

// console.log(mergeSorted([1, 2, 3], []));
// // Expected: [1, 2, 3]
// // Actual: [1, 2, 3, undefined, undefined, undefined]

// console.log(mergeSorted([], [4, 5, 6]));
// // Expected: [4, 5, 6]
// // Actual: [4, 5, 6]  ✓


// --------- Problem 5: Calculate Average by Category
// Buggy:
function calculateAverages(data) {
  let sums = {};
  let counts = {};
  
  for(let i = 0; i < data.length; i++){
    let cat = data[i].category;
    let val = data[i].value;
    
    if(!sums[cat]){
      sums[cat] = 0;
      counts[cat] = 0;
    }
    
    sums[cat] += val;
    counts[cat]++;
  }
  
  let averages = {};
  for(let cat in sums){
    averages[cat] = Math.round(sums[cat] / counts[cat] * 100) / 100;
  }
  
  return averages;
}

//Actual:
function calculateAverages(data) {
  let sums = {};
  let counts = {};
  
  for(let i = 0; i < data.length; i++){
    let cat = data[i].category;
    let val = data[i].value;
    
    if(val !== null && val !== undefined){
        if(!sums[cat]){
        sums[cat] = 0;
        counts[cat] = 0;
        }
        
        sums[cat] += (val || 0); // Probably not even needed
        counts[cat]++;
    }
  }
  
  let averages = {};
  for(let cat in sums){
    averages[cat] = Math.round(sums[cat] / counts[cat] * 100) / 100; // Just means round the result to 2 decimal
  }
  
  return averages;
}


let data = [
  {category: 'A', value: 10},
  {category: 'B', value: 20},
  {category: 'A', value: 30},
  {category: 'B', value: null},
  {category: 'A', value: 15}
];

console.log(calculateAverages(data));
// Expected: { A: 18.33, B: 20 }
// Actual: { A: 11, B: 6.67 }

let data2 = [
  {category: 'X', value: null},
  {category: 'X', value: undefined}
];

console.log(calculateAverages(data2));
// Expected: {}
// Actual: { X: 0 }
