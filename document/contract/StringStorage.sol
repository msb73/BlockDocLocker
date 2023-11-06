// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StringStorage {
    string public storedString;

    event StringStored(string newValue);

    function storeString(string memory newValue) public {
        storedString = newValue;
        emit StringStored(newValue);
    }
}
