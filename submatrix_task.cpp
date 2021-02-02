// C++ program to find largest rectangle with all 1s 
// in a binary matrix 

// THIS IS MODIFICATION OF THE ORIGINAL CODE:
//https://tutorialspoint.dev/data-structure/matrix-archives/maximum-size-rectangle-binary-sub-matrix-1s

#include <stack>
#include <algorithm>
#include <unordered_map>

using namespace std;

// Rows and columns in input matrix 
#define R 4 
#define C 5 

// Finds the maximum area under the histogram represented 
// by histogram.  See below article for details. 
// https://tutorialspoint.dev/slugresolver/largest-rectangle-under-histogram/ 
int maxHist(int row[], int &left, int &right, int &height)
{
    // Create an empty stack. The stack holds indexes of 
    // hist[] array/ The bars stored in stack are always 
    // in increasing order of their heights. 
    stack<int> result;

    int top_val;     // Top of stack 

    int max_area = 0; // Initialize max area in current 
                      // row (or histogram) 

    int area = 0;    // Initialize area with current top 

    // Run through all bars of given histogram (or row) 
    int i = 0;
    while (i < C)
    {
        // If this bar is higher than the bar on top stack, 
        // push it to stack 
        if (result.empty() || row[result.top()] <= row[i])
        {
            result.push(i++);
        }

        else
        {
            // If this bar is lower than top of stack, then 
            // calculate area of rectangle with stack top as 
            // the smallest (or minimum height) bar. 'i' is 
            // 'right index' for the top and element before 
            // top in stack is 'left index' 
            top_val = row[result.top()];
            result.pop();
            area = top_val * i;

            if (!result.empty())
            {
                area = top_val * (i - result.top() - 1);
            }
            //max_area = max(area, max_area);
            if (area > max_area)
            {
                max_area = area;
                left = result.empty() ? 0 : result.top() + 1; right = i - 1; height = top_val;
            }
        }
    }

    // Now pop the remaining bars from stack and calculate area 
    // with every popped bar as the smallest bar 
    while (!result.empty())
    {
        top_val = row[result.top()];
        result.pop();
        area = top_val * i;
        if (!result.empty())
        {
            area = top_val * (i - result.top() - 1);
        }

        //max_area = max(area, max_area);
        if(area > max_area)
        {
            max_area = area;
            left = result.empty() ? 0 : result.top() + 1; right = i - 1; height = top_val;
        }
    }
    return max_area;
}

// Returns area of the largest rectangle with all 1s in A[][] 
int maxRectangle(int A[][C], int &left, int &top, int &right, int &bottom)
{
    // Calculate area for first row and initialize it as 
    // result
    int left_ = 0, right_ = 0, height_ = 0;
    int result = maxHist(A[0], left, right, height_);
    top = 0; bottom = 0;

    // iterate over row to find maximum rectangular area 
    // considering each row as histogram 
    for (int i = 1; i < R; i++)
    {
        for (int j = 0; j < C; j++)
        {
            if (A[i][j])
            {
                A[i][j] += A[i - 1][j];
            }
        }

        // Update result if area with current row (as last row) 
        // of rectangle) is more
        int result_ = maxHist(A[i], left_, right_, height_);
        if (result_ > result)
        {
            result = result_;
            left = left_; right = right_; top = i + 1 - height_; bottom = i;
        }
    }

    return result;
}

int main()
{
    int A[][C] = {
        {1,1,1,1,0},
        {0,1,1,1,1},
        {1,1,1,1,1},
        {0,1,1,0,0}
    };

    int top, left, right, bottom;
    int S = maxRectangle(A, left, top, right, bottom);

    printf("(%d,%d)-(%d,%d), S = %d", left, top, right, bottom, S);

    return 0;
}
