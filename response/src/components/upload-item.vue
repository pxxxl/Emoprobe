<template>
    <div class="select-no dis-flex">
    <div class="dis-flex file align-items-center">
        <slot name="file" id="item"></slot>
    </div>
    <div class="delete center-flex">
        <slot name="elprogress"></slot>
    </div>
    </div>
</template>

<style>
.file{
    flex: 5;
}
.delete{
    flex: 1;
}
</style>