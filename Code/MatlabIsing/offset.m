function [ off ] = offset( n,N )
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here
off= N + (n-1)*(N-2) - (n-1)*(n-2)/2 -1 ;
end

