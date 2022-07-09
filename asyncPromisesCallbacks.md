# Async in JS

## Promises

- A promise is a special JavaScript object that represents the eventual completion (or failure) of an asynchronous operation and its resulting value.
- Now the state of the obj can be :-

     - Pending
     - Fulfilled
     - rejected

- A Promise is a proxy for a value not necessarily known when the promise is created.It allows you to associate handlers with an asynchronous action's eventual success value or failure reason
- Instead of immediately returning the final value, the asynchronous method returns a promise to supply the value at some point in the future.
- Its kind of replaces callbacks with more readable code since callbacks would create callback hell leading to unmanagable code.


````js
let Proms = new Promise((resolve, reject) => {

    const a = 1;

    if(a == 1){
        resolve(a)
    }else {
        reject("failed")
    }
})

// Its returing an obj with the state of the task and not the value immediatly because but a promise to return the value when its resolved

// So "then" receives a function to be executed if and when the promise is fulfilled (after pending state) and "catch" (after pending state) has the same but when the promise is rejected.

Proms.then((res) => {
    console.log(res);
}).catch(e => {
    console.log(e)
})

````
![alt text](/resources/promises-1.png "RDS")

- Line 12 is wrong cause we are not returing the promise explicitly so we couldn't chain it.

![alt text](/resources/promises.png "RDS")

- Here we are able to chain bunch of promises together.
- All the errors can be handled by a single catch, so we don't need specific callbacks to handle specific errors of each callback.

[Source](https://www.youtube.com/playlist?list=PLRqwX-V7Uu6bKLPQvPRNNE65kBL62mVfx)

## Promise.all




[Source](https://medium.com/@copperwall/implementing-promise-all-575a07db509a)