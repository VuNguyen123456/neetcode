let orders = [
  {orderId: 1, customer: 'Alice', items: ['laptop', 'mouse'], total: 1200, status: 'delivered'},
  {orderId: 2, customer: 'Bob', items: ['keyboard'], total: 100, status: 'pending'},
  {orderId: 3, customer: 'Alice', items: ['monitor', 'cable'], total: 400, status: 'shipped'},
  {orderId: 4, customer: 'Charlie', items: ['laptop', 'bag'], total: 1300, status: 'delivered'},
  {orderId: 5, customer: 'Bob', items: ['mouse', 'pad'], total: 50, status: 'delivered'},
  {orderId: 6, customer: 'Alice', items: ['keyboard', 'mouse'], total: 150, status: 'pending'},
  {orderId: 7, customer: 'Charlie', items: ['monitor'], total: 300, status: 'shipped'}
];

function getCustomerSpending(orders) {
  return orders.reduce((a,n) => {
    if(!a[n.customer]){
        a[n.customer] = 0
    }
    a[n.customer] += n.total
    return a
  }, {})
}

console.log(getCustomerSpending(orders));

function getTopItems(orders, topN) {
  // Return array of [item, count] sorted by count descending
  let tempDic = orders.reduce((a,n) => {
    for (let i = 0; i < n.items.length; i++){
        if(!a[n.items[i]]){
            a[n.items[i]] = 0
        }
        a[n.items[i]] += 1
    }
    return a
  }, {})
  let arr = []
  Object.keys(tempDic).forEach(key => {
    arr.push([key, tempDic[key]])
  })
  console.log(arr)
  return arr.sort((a, b) => b[1] - a[1]).slice(0, topN) // this is descending
}

function getRevenueByStatus(orders) {
  return orders.reduce((a,n) => {
    if(!a[n.status]){
        a[n.status] = 0
    }
    a[n.status] +=  n.total
    return a
  },{})
}

function getQualifiedCustomers(orders) {
  // Return array of customer names
  let res = []
  orders.reduce((a,n) => {
    if(!a[n.customer]){
        a[n.customer] = {ordersNum : 0, totalSpend: 0, atleastOneDeli: false}
    }
    a[n.customer].ordersNum += 1
    a[n.customer].totalSpend += n.total
    if(n.status === "delivered"){
        a[n.customer].atleastOneDeli = true
    }
    if(a[n.customer].ordersNum >= 2 && a[n.customer].totalSpend >= 500 && a[n.customer].atleastOneDeli === true){
        res.push(n.customer)
    }
    return a
  }, {})
  return [...new Set(res)]; // Get rid of repeat
}

function getOrderDashboard(orders) {
    let totalRev = 0
    orders.forEach(n => totalRev += n.total)
    let cusCount = Object.keys(getCustomerSpending(orders)).length
    let bestCus = { name: '...', spending: 0 }
    let spending = getCustomerSpending(orders);
    Object.keys(spending).forEach(key => {
        if(bestCus.spending < spending[key]){
            bestCus.spending = spending[key]
            bestCus.name = key
        }
    })
    let deliveredPercent = orders.reduce((a,n) => {
        if(n.status === "delivered"){
            a += 1
        }
        return a
    }, 0)
    deliveredPercent = (deliveredPercent/orders.length) * 100
    return {
        totalRevenue: totalRev,
        totalOrders: orders.length,
        averageOrderValue: totalRev/orders.length,
        customerCount: cusCount,
        statusBreakdown: getRevenueByStatus(orders),
        topCustomer: bestCus,
        topItems: getTopItems(orders, 3),
        deliveryRate: deliveredPercent
    };
}

// console.log(getQualifiedCustomers(orders));
// Expected: ['Alice', 'Charlie']
// Bob only has $150 total (< $500)
// console.log(getRevenueByStatus(orders));
// // Expected: { delivered: 2550, pending: 250, shipped: 700 }
// console.log(getTopItems(orders, 3));
// Expected: [['mouse', 3], ['laptop', 2], ['keyboard', 2]]
// or [['mouse', 3], ['keyboard', 2], ['laptop', 2]] - order of ties doesn't matter
