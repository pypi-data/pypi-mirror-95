/*
    Copyright (c) 2005-2019 Intel Corporation

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

#include "harness_allocator_overload.h"
#define HARNESS_NO_PARSE_COMMAND_LINE 1
#define __TBB_NO_IMPLICIT_LINKAGE 1

#include "harness.h"

#if !HARNESS_SKIP_TEST && TBB_USE_EXCEPTIONS

#include "harness_tbb_independence.h"
#include "harness_assert.h"
#include "harness_barrier.h"

#include "../tbb/tls.h"

tbb::internal::tls<bool> new_handler_called;
void customNewHandler() {
    new_handler_called = true;
    throw std::bad_alloc();
}

// Return true if operator new threw exception
bool allocateWithException(size_t big_mem) {
    bool exception_caught = false;
    try {
        // Allocate big array (should throw exception)
        char* volatile big_array = new char[big_mem];
        // If succeeded, double the size (unless it overflows) and recursively retry
        if (big_mem * 2 > big_mem) {
            exception_caught = allocateWithException(big_mem * 2);
        }
        delete[] big_array;
    } catch (const std::bad_alloc&) {
        ASSERT(new_handler_called, "User provided new_handler was not called.");
        exception_caught = true;
    }
    return exception_caught;
}

class AllocLoopBody : NoAssign {
public:
    void operator()(int) const {
        size_t BIG_MEM = 100 * 1024 * 1024;
        new_handler_called = false;
        ASSERT(allocateWithException(BIG_MEM), "Operator new did not throw bad_alloc.");
    }
};

int TestMain() {
#if __TBB_CPP11_GET_NEW_HANDLER_PRESENT
    std::new_handler default_handler = std::get_new_handler();
    ASSERT(default_handler == NULL, "No handler should be set at this point.");
#endif
    // Define the handler for new operations
    std::set_new_handler(customNewHandler);
    // Run the test
    NativeParallelFor(8, AllocLoopBody());
    // Undo custom handler
    std::set_new_handler(0);
    return Harness::Done;
}
#else
int TestMain() {
    return Harness::Skipped;
}
#endif // !HARNESS_SKIP_TEST && TBB_USE_EXCEPTIONS
