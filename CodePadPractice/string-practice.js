function isPalindrome(str) {
  str = str.toLowerCase().replace(/ /g, ''); // Remove spaces, lowercase
  let halfLen = Math.floor(str.length / 2)
  for(let left = 0; left < halfLen; left++){
    right = (str.length - 1) - left
    if(str[left] !== str[right]){
      return false
    }
  }
  return true

}

console.log(isPalindrome("racecar"));  // true
console.log(isPalindrome("hello"));    // false
console.log(isPalindrome("noon"));     // true
console.log(isPalindrome("A man a plan a canal Panama")); // true (ignoring spaces/caps)

function areAnagrams(str1, str2) {
  let s1 = str1.split('').sort().join('');  // "eilnst"
  let s2 = str2.split('').sort().join('');  // "eilnst"
  return s1 === s2;  // Compare strings directly
}

console.log(areAnagrams("listen", "silent"));  // true
console.log(areAnagrams("hello", "world"));    // false
console.log(areAnagrams("triangle", "integral")); // true

function countCharacters(str) {
  let countChar = {}
  for(let i = 0; i < str.length; i++){
    if(!countChar[str[i]]){
        countChar[str[i]] = 0
    }
    countChar[str[i]] += 1
  }
  return countChar
}

console.log(countCharacters("hello"));
// Should output: { h: 1, e: 1, l: 2, o: 1 }


function firstNonRepeating(str) {
  // Return first character that appears only once
  let dic = countCharacters(str)
  for(let i = 0; i < str.length; i++){
    if(dic[str[i]] === 1){
        return str[i]
    }
  }
  return null
}

console.log(firstNonRepeating("leetcode"));  // "l"
console.log(firstNonRepeating("loveleetcode")); // "v"
console.log(firstNonRepeating("aabb"));      // null or ""

function removeDuplicates(str) {
  // Return string with duplicates removed, keep first occurrence
  const mySet = new Set();
  let result = "";
  for(let i = 0; i < str.length; i++){
    if(!mySet.has(str[i])){
        mySet.add(str[i])
        result += str[i]
    }
  }
  return result
}

console.log(removeDuplicates("hello"));     // "helo"
console.log(removeDuplicates("aabbcc"));    // "abc"
