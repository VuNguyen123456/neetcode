let posts = [
  {id: 1, user: 'alice', content: 'Hello world!', likes: 15, comments: 3, hashtags: ['coding', 'js']},
  {id: 2, user: 'bob', content: 'Love coding', likes: 8, comments: 1, hashtags: ['coding']},
  {id: 3, user: 'alice', content: 'New project', likes: 25, comments: 7, hashtags: ['project', 'js']},
  {id: 4, user: 'charlie', content: 'Learning JS', likes: 12, comments: 2, hashtags: ['js', 'learning']},
  {id: 5, user: 'bob', content: 'Code review', likes: 20, comments: 5, hashtags: ['coding', 'review']},
  {id: 6, user: 'alice', content: 'Tech talk', likes: 30, comments: 8, hashtags: ['tech']},
  {id: 7, user: 'charlie', content: 'Bug fixes', likes: 5, comments: 0, hashtags: ['coding', 'bugs']}
];

function getUserEngagement(posts) {
  return posts.reduce((a,n) => {
    if(!a[n.user]){
        a[n.user] = 0
    }
    a[n.user] += n.likes + (n.comments * 2)
    return a
  }, {})
}

function getTrendingHashtags(posts, topN) {
  // Return array of [hashtag, totalLikes] sorted descending
  let tagLikes = posts.reduce((a,n) => {
    for(let i = 0; i < n.hashtags.length; i++){
        if(!a[n.hashtags[i]]){
            a[n.hashtags[i]] = 0
        }
        a[n.hashtags[i]] += n.likes
    }
    return a
  }, {})
  let arr = []
  Object.keys(tagLikes).forEach(key => {
    arr.push([key, tagLikes[key]])
  })
  return arr.sort((a, b) => b[1] - a[1]).slice(0, topN)
}

function getAvgLikes(posts) {
  return posts.reduce((a,n) => {
    a += n.likes
    return a
  }, 0) / posts.length
}

function getAvgComments(posts) {
  return posts.reduce((a,n) => {
    a += n.comments
    return a
  }, 0) / posts.length
}

function getTopUser(posts){
    let userEngagement = posts.reduce((a,n) => {
        if(!a[n.user]){
            a[n.user] = [0,0]
        }
        a[n.user][0] += 1
        a[n.user][1] += n.likes
        return a
    }, {}) // {"Bob": [postNum, totalLike]}
    let topUser = { user: '...', postCount: 0, totalLikes:0}
    Object.keys(userEngagement).forEach(key => {
        if(topUser.totalLikes < userEngagement[key][1]){
            topUser.user = key
            topUser.postCount = userEngagement[key][0]
            topUser.totalLikes = userEngagement[key][1]
        }
    })
    return topUser
}

function getViralPosts(posts) {
  let res = []
  let avgL = getAvgLikes(posts)
  let avgC = getAvgComments(posts)
  for(let i = 0; i < posts.length; i++){
    if(posts[i].likes > avgL && posts[i].comments > avgC){
        res.push(posts[i].id)
    }
  }
  return res
}

function getHashtagsPost(posts) {
  // Return array of [hashtag, totalLikes] sorted descending
  return posts.reduce((a,n) => {
    for(let i = 0; i < n.hashtags.length; i++){
        if(!a[n.hashtags[i]]){
            a[n.hashtags[i]] = 0
        }
        a[n.hashtags[i]] += 1
    }
    return a
  }, {})
}

function getContentAnalytics(posts) {
  return {
    totalPosts: posts.length,
    totalEngagement: posts.reduce((a, n) => a + n.likes + n.comments, 0),
    topUser: getTopUser(posts),
    engagementRate: (getAvgComments(posts) / getAvgLikes(posts)) * 100,
    hashtagDistribution: getHashtagsPost(posts),
    viralPostsCount: getViralPosts(posts).length
  };
}
// console.log(getViralPosts(posts));
// Average likes: (15+8+25+12+20+30+5)/7 = 16.43
// Average comments: (3+1+7+2+5+8+0)/7 = 3.71
// Posts above both: id 3 (25 likes, 7 comments), id 6 (30 likes, 8 comments)
// Expected: [3, 6]

// console.log(getTrendingHashtags(posts, 3));
// Expected: [['coding', 60], ['js', 52], ['project', 25]]
// coding: posts 1,2,5,7 = 15+8+20+5 = 48... wait let me recalc
// console.log(getUserEngagement(posts));
// Expected: { alice: 106, bob: 40, charlie: 21 }
