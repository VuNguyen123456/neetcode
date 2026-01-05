// Dictionary of products
let products = [
  {name: 'Apple', category: 'Fruit', price: 1.2, quantity: 5},
  {name: 'Banana', category: 'Fruit', price: 0.5, quantity: 10},
  {name: 'Carrot', category: 'Vegetable', price: 0.8, quantity: 7},
  {name: 'Broccoli', category: 'Vegetable', price: 1.5, quantity: 3},
  {name: 'Orange', category: 'Fruit', price: 0.9, quantity: 8},
  {name: 'Lettuce', category: 'Vegetable', price: 1.0, quantity: 4}
];

function getTotalRevenue(products){
    // Revenue for all product => sum of all
    return products.reduce((acc, n) => {
        let curProdRev = n.price * n.quantity
        acc += curProdRev 
        return acc
    }, 0)
}

function getMostExpensiveItem(product){
    return product.reduce((acc,n) => {
        let accR =  acc.price*acc.quantity
        let curR = n.price*n.quantity
        if(accR < curR){
            acc = n
        }
        return acc // This return the object not the 
    })
}

// a function that groups products by category and calculates the total revenue for each category.
function groupByCategory(){
    return products.reduce((acc, n) => {
        let rev = n.price * n.quantity;
        // Need to use acc and do stuff to it because it retain everyloop while others let doesn't!!

        // If category doesn't exist yet, create it
        if(!acc[n.category]){
            acc[n.category] = { totalRevenue: 0, items: [] };
        }

        acc[n.category].totalRevenue += rev;
        acc[n.category].items.push(n.name);

        return acc;
    },{})
}

// so the 1 liner automatically retunr?
// Rule of Thumb:
// No {} → automatic return
// With {} → must write return
function getHighRevenueItems(products, threshold) {
  return products.filter(n => (n.price * n.quantity) > threshold);
}

function getSummary(products) {
  // Your code here
  // Should return an object with:
  // - totalRevenue: sum of all revenues
  // - itemCount: total number of products
  // - averagePrice: average price across all products
  // - categories: array of unique category names
  // - highestRevenueItem: the product with highest revenue
  let totalPrice = 0
  return products.reduce((a,n) => {
    let curRevenue = n.price * n.quantity
    a.totalRevenue += curRevenue
    totalPrice += n.price
    a.averagePrice = totalPrice / a.itemCount
    if(!a.categories.includes(n.category)){
        a.categories.push(n.category)
    }
    if(a.highestRevenueItem.price * a.highestRevenueItem.quantity < curRevenue){
        a.highestRevenueItem = n
    }
    return a

  }, {totalRevenue: 0,
  itemCount: products.length,
  averagePrice: 0,
  categories: [],
  highestRevenueItem: products[0]})
}

console.log(getSummary(products));
// console.log(getTotalRevenue(products));
// console.log(getMostExpensiveItem(products)); 
// console.log(groupByCategory(products));
// console.log(getHighRevenueItems(products, 5));
