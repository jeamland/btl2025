const reps = document.getElementById("ballot-reps");
if (reps !== null) {
    ballotManager(reps);
}

const senate = document.getElementById("ballot-senate");
if (senate !== null) {
    ballotManager(senate);
}

const errorClasses = ["border-red-300", "active:border-red-300", "text-red-300"];

function ballotManager(ballot: HTMLElement) {
    let maxPositions = 0;
    const inputs: HTMLInputElement[] = [];

    ballot.querySelectorAll("input").forEach((input) => {
        input.addEventListener("change", (event) => {
            if (!(event.target instanceof HTMLInputElement)) {
                return;
            }
            const target = event.target!;

            const value = parseInt(target.value);
            console.log(target.name, "change to", value);

            if (value <= 0 || value > maxPositions) {
                errorClasses.forEach((cls) => target.classList.add(cls));
                return;
            }

            errorClasses.forEach((cls) => target.classList.remove(cls));

            const index = inputs.findIndex((i) => i.name == target.name);
            console.log(target.name, index, "->", value - 1);
            inputs.splice(index, 1);
            inputs.splice(value - 1, 0, target);
            console.log(inputs.map((i) => i.name));

            const rows: HTMLElement[] = [];

            inputs.forEach((i, idx) => {
                const value = idx + 1;
                console.log(i.name, value);

                if (i.value != value.toString()) {
                    i.value = value.toString();
                }

                const row = i.parentElement!;

                rows.push(row);
                row.classList.forEach((cls) => {
                    if (cls.startsWith("order-")) {
                        row.classList.remove(cls);
                    }
                });
                row.classList.add("order-" + value);
            });

            // const order = inputs.map((input) => {
            //     const n = parseInt(input.name.replace("reps-", ""))!;
            //     return n.toString(16);
            // });
            // console.log(order.join(''));
            // document.location.hash = order.join('');
        });
        inputs.push(input);
        maxPositions += 1;
    });

    // if (document.location.hash.length == maxPositions + 1) {
    //     const order = document.location.hash.substring(1).split("").map((c) => {
    //         return parseInt(c, 16)!;
    //     });
    //     console.log(order);
    // }
}
