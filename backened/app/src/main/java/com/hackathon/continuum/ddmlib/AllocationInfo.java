/*
 * Copyright (C) 2008 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.hackathon.continuum.ddmlib;

/**
 * Holds an Allocation information.
 */
public class AllocationInfo implements Comparable<AllocationInfo>, IStackTraceInfo {
    private String mAllocatedClass;
    private int mAllocationSize;
    private short mThreadId;
    private StackTraceElement[] mStackTrace;

    /*
     * Simple constructor.
     */
    AllocationInfo(String allocatedClass, int allocationSize,
        short threadId, StackTraceElement[] stackTrace) {
        mAllocatedClass = allocatedClass;
        mAllocationSize = allocationSize;
        mThreadId = threadId;
        mStackTrace = stackTrace;
    }
    
    /**
     * Returns the name of the allocated class.
     */
    public String getAllocatedClass() {
        return mAllocatedClass;
    }

    /**
     * Returns the size of the allocation.
     */
    public int getSize() {
        return mAllocationSize;
    }

    /**
     * Returns the id of the thread that performed the allocation.
     */
    public short getThreadId() {
        return mThreadId;
    }

    /*
     * (non-Javadoc)
     * @see com.android.ddmlib.IStackTraceInfo#getStackTrace()
     */
    public StackTraceElement[] getStackTrace() {
        return mStackTrace;
    }

    public int compareTo(AllocationInfo otherAlloc) {
        return otherAlloc.mAllocationSize - mAllocationSize;
    }
}
