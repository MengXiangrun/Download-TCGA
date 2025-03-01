    def GCN_node_class_random_split(self, node_label: torch.Tensor):
        num_train = 20
        num_valid = 500
        num_test = 1000

        device = node_label.device
        dtype = node_label.dtype

        if torch.is_tensor(node_label):
            node_label = node_label.detach().cpu().numpy().tolist()

        node_label = pd.DataFrame(node_label, columns=['label'])
        node_label = node_label.reset_index(drop=False, names='node')
        node_label = node_label.sort_values(by='label', ascending=True)

        # random shuffle
        node_label = node_label.sample(frac=1)
        node_label = node_label.sort_values(by='label', ascending=True)
        node_label = node_label.reset_index(drop=True)

        unique_label = node_label['label'].unique()

        train_node_label_list = []
        other_node_label_list = []
        for label in unique_label:
            train_node_label = node_label[node_label['label'] == label].head(num_train)
            train_node_label = train_node_label.sort_values(by='node', ascending=True)
            train_node_label_list.append(train_node_label)

            other_node_label = node_label[node_label['label'] == label].iloc[num_train:]
            other_node_label = other_node_label.sort_values(by='node', ascending=True)
            other_node_label_list.append(other_node_label)

        other_node_label = pd.concat(other_node_label_list, axis=0)
        other_node_label = other_node_label.reset_index(drop=True)

        # random shuffle
        other_node_label = other_node_label.sample(frac=1)

        valid_node_label = other_node_label.head(num_valid)
        test_node_label = other_node_label.iloc[num_valid:num_valid + num_test]

        valid_node_label_list = []
        test_node_label_list = []
        for label in unique_label:
            sort_valid_node_label = valid_node_label[valid_node_label['label'] == label]
            sort_valid_node_label = sort_valid_node_label.sort_values(by='node', ascending=True)
            valid_node_label_list.append(sort_valid_node_label)

            sort_test_node_label = test_node_label[test_node_label['label'] == label]
            sort_test_node_label = sort_test_node_label.sort_values(by='node', ascending=True)
            test_node_label_list.append(sort_test_node_label)

        train_node_label = pd.concat(train_node_label_list, axis=0)
        valid_node_label = pd.concat(valid_node_label_list, axis=0)
        test_node_label = pd.concat(test_node_label_list, axis=0)

        train_data_statistics = ['train']
        valid_data_statistics = ['valid']
        test_data_statistics = ['test']
        node_class = ['data_type']
        for label in unique_label:
            node_class.append(str(label))

            num_node = train_node_label[train_node_label['label'] == label].shape[0]
            train_data_statistics.append(num_node)

            num_node = valid_node_label[valid_node_label['label'] == label].shape[0]
            valid_data_statistics.append(num_node)

            num_node = test_node_label[test_node_label['label'] == label].shape[0]
            test_data_statistics.append(num_node)
        data_statistics = [train_data_statistics, valid_data_statistics, test_data_statistics]
        self.data_statistics = pd.DataFrame(data_statistics, columns=node_class)

        train_node = train_node_label['node'].values
        valid_node = valid_node_label['node'].values
        test_node = test_node_label['node'].values

        train_node = torch.tensor(train_node, device=device, dtype=dtype)
        valid_node = torch.tensor(valid_node, device=device, dtype=dtype)
        test_node = torch.tensor(test_node, device=device, dtype=dtype)

        return [train_node, valid_node, test_node]

    def Balance_node_class_random_split(self, node_label: torch.Tensor):
        num_train = 20
        num_valid = 500
        num_test = 1000

        device = node_label.device
        dtype = node_label.dtype

        if torch.is_tensor(node_label):
            node_label = node_label.detach().cpu().numpy().tolist()

        node_label = pd.DataFrame(node_label, columns=['label'])
        node_label = node_label.reset_index(drop=False, names='node')
        node_label = node_label.sort_values(by='label', ascending=True)

        # random shuffle
        node_label = node_label.sample(frac=1)
        node_label = node_label.sort_values(by='label', ascending=True)
        node_label = node_label.reset_index(drop=True)

        unique_label = node_label['label'].unique()

        num_valid = num_valid // len(unique_label)
        num_test = num_test // len(unique_label)

        train_node_label_list = []
        valid_node_label_list = []
        test_node_label_list = []
        for label in unique_label:
            start = 0
            end = num_train
            train_node_label = node_label[node_label['label'] == label].iloc[start:end]
            train_node_label = train_node_label.sort_values(by='node', ascending=True)
            train_node_label_list.append(train_node_label)

            start = num_train
            end = num_train + num_valid
            valid_node_label = node_label[node_label['label'] == label].iloc[start:end]
            valid_node_label = valid_node_label.sort_values(by='node', ascending=True)
            valid_node_label_list.append(valid_node_label)

            start = num_train + num_valid
            end = num_train + num_valid + num_test
            test_node_label = node_label[node_label['label'] == label].iloc[start:end]
            test_node_label = test_node_label.sort_values(by='node', ascending=True)
            test_node_label_list.append(test_node_label)

        train_node_label = pd.concat(train_node_label_list, axis=0)
        valid_node_label = pd.concat(valid_node_label_list, axis=0)
        test_node_label = pd.concat(test_node_label_list, axis=0)

        train_data_statistics = ['train']
        valid_data_statistics = ['valid']
        test_data_statistics = ['test']
        node_class = ['data_type']
        for label in unique_label:
            node_class.append(str(label))

            num_node = train_node_label[train_node_label['label'] == label].shape[0]
            train_data_statistics.append(num_node)

            num_node = valid_node_label[valid_node_label['label'] == label].shape[0]
            valid_data_statistics.append(num_node)

            num_node = test_node_label[test_node_label['label'] == label].shape[0]
            test_data_statistics.append(num_node)
        data_statistics = [train_data_statistics, valid_data_statistics, test_data_statistics]
        self.data_statistics = pd.DataFrame(data_statistics, columns=node_class)

        train_node = train_node_label['node'].values
        valid_node = valid_node_label['node'].values
        test_node = test_node_label['node'].values

        train_node = torch.tensor(train_node, device=device, dtype=dtype)
        valid_node = torch.tensor(valid_node, device=device, dtype=dtype)
        test_node = torch.tensor(test_node, device=device, dtype=dtype)

        return [train_node, valid_node, test_node]
