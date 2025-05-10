#include <iostream>

void CStylePointer() {
    std::cout << "\n\n==== BASIC C-style RAW POINTER - Declaration ====\n";
    
    int int1 = 13;
    int int2 = 5;

    int* int1Ptr = &int1;
    int* int2Ptr = &int2;

    // Even if another pointer points to the same value, it points to the same address of int1,
    // but the pointer location itself is different.
    int* int3Ptr = &int1; 

    std::cout << "int1Ptr address: " << &int1Ptr << "\n";
    std::cout << "int2Ptr address: " << &int2Ptr << "\n";
    std::cout << "int3Ptr address: " << &int3Ptr << "\n";

    std::cout << "\n\n==== BASIC C-style RAW POINTER - Swap Values ====\n";
    
    std::cout << "Before swap:\n";
    std::cout << "int1Ptr points to " << int1Ptr << " with value: " << *int1Ptr << "\n";
    std::cout << "int2Ptr points to " << int2Ptr << " with value: " << *int2Ptr << "\n";

    // Swapping values
    int tempInt = *int1Ptr;  
    *int1Ptr = *int2Ptr;  
    *int2Ptr = tempInt;  

    std::cout << "After swap:\n";
    std::cout << "int1Ptr points to " << int1Ptr << " with value: " << *int1Ptr << "\n";
    std::cout << "int2Ptr points to " << int2Ptr << " with value: " << *int2Ptr << "\n";

    std::cout << "int3Ptr still points to int1, so its value also changed: " << *int3Ptr << "\n";


    std::cout << "\n\n==== BASIC C-style RAW POINTER - 1D Array and Pointer Arithmetic ====\n";

    int array1D[5] = {0, 1, 2, 3, 4};
    int* arr1DPtr = array1D;
    int* arr1DPtrAlias = &array1D[0];

    std::cout << "arr1DPtr : " << arr1DPtr << '\n';
    std::cout << "arr1DPtrAlias : " << arr1DPtrAlias << '\n';

    // Pointer Arithmetic
    std::cout << "Pointer arithmetic:\n";
    std::cout << "arr1DPtr is at address: " << arr1DPtr << " with value: " << *arr1DPtr << '\n';
    arr1DPtr++;  
    std::cout << "After ++arr1DPtr, new address: " << arr1DPtr << " with value: " << *arr1DPtr << '\n';

    std::cout << "Value at arr1DPtr + 2: " << *(arr1DPtr + 2) << " (moves forward by 2 integers)\n";

    // Iterate through array using pointer arithmetic
    std::cout << "Iterating array using pointer arithmetic: ";
    for (int offset = 0; offset < 5; ++offset) {
        std::cout << *(array1D + offset) << " ";
    }
    std::cout << "\n";


    std::cout << "\n\n==== BASIC C-style RAW POINTER - 2D Array ====\n";

    int array2D[2][5] = {{0, 1, 2, 3, 4}, {5, 6, 7, 8, 9}};

    std::cout << "**array2D points to: " << **array2D << " (first element: 0)\n";
    std::cout << "**(array2D + 1) points to: " << **(array2D + 1) << " (first element of second row: 5)\n";
    std::cout << "*((*array2D) + 5) points to: " << *((*array2D) + 5) << " (linear memory access to second row first element: 5)\n";
    std::cout << "*(*(array2D + 1) + 2) points to: " << *(*(array2D + 1) + 2) << " (element at row 1, col 2: 7)\n";

    // Pointer Aliases for Rows
    int* arr2DPtr0 = array2D[0];
    int* arr2DPtr0Alias = *array2D;
    int* arr2DPtr1 = array2D[1];

    std::cout << "array2D base address: " << array2D << "\n";
    std::cout << "arr2DPtr0 (first row): " << arr2DPtr0 << "\n";
    std::cout << "arr2DPtr0Alias (alias for first row): " << arr2DPtr0Alias << "\n";
    std::cout << "arr2DPtr1 (second row): " << arr2DPtr1 << "\n";

    std::cout << "array2D[1] (second row): " << array2D[1] << "\n";
    std::cout << "(array2D[0] + 5) (next row start): " << (array2D[0] + 5) << "\n";
    std::cout << "(array2D + 1) (pointer to second row): " << (array2D + 1) << "\n";
}


void CPPStylePointer()
{
    // don't use weak pointer.
    // use unique_pointer (not use shared_pointer as possible)
}

int main()
{
    CStylePointer();
    CPPStylePointer();
};