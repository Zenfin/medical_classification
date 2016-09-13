def get_combos(self, y_train):
    outcomes = set(y_train)
    outcome_combos = permutations(outcomes)
    model_combos = product(ALL_CLASSIFIERS.keys(),
                           repeat=len(outcomes) - 1)
    return list(outcome_combos), list(model_combos)


def processing(self, threads):
    for thread in threads:
        if thread.is_alive():
            return True


def spawn_threads(chunk_size, *train_test_data):
    outcome_combos, model_combos = get_combos(train_test_data[1])
    outcome_chunks = [
        outcome_combos[i:i + chunk_size]
        for i in xrange(0, len(outcome_combos), chunk_size)
    ]
    threads = []
    for chunk in outcome_chunks:
        args = [chunk, model_combos] + list(train_test_data)
        threads.append(threading.Thread(target=run, args=args))
    return threads


def run(outcome_combos, model_combos, *train_test_data):
    best = None
    for outcomes in outcome_combos:
        for combo in model_combos:
            tracker = predict_combo(combo, outcomes, *train_test_data)
            if not best or tracker.accuracy > best.accuracy:
                best = tracker
    with open("best_cascade.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([tracker.accuracy, tracker.algo_name])


def predict_combo(self, combo, outcomes, x_training, y_training, x_test, y_test):
    name = ",".join(list(combo) + map(str, outcomes))
    self.classifiers = [
        (outcomes[i], deepcopy(self.all_classifiers[k]))
        for i, k in enumerate(combo)
    ]
    self.fit(x_training, y_training)
    predicted_vals = self.predict(x_test)
    tracker = Tester(predicted_vals, OUTCOMES, name)
    tracker.predict(y_training, y_test)
    print(accuracy_msg(tracker))
    return tracker


def accuracy_msg(tracker):
    return "Accuracy: {}% - {}".format(
        round(tracker.accuracy), tracker.algo_name)


def all_combo_classifier(chunk_size, *train_test_data):
    """Multithreading: Write highest value classifiers from chunks"""
    threads = spawn_threads(chunk_size, *train_test_data)
    for thread in threads:
        thread.start()
    while processing(threads):
        sleep(5)
    print("Done")


def all_combo_classifier_from_file(self, filename, shuffle=False, ignore=[],
                                   chunk_size=3):
    all_combo_classifier(chunk_size, *train_test(
        load_data(filename),
        train_percent=TRAIN_PERCENT,
        shuffle=shuffle,
        ignore=ignore
    ))
